package proxy

import (
	"bytes"
	"crypto/md5"
	"encoding/json"
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"net/http/httputil"
	"net/url"
	"sort"
	"strings"
	"sync"
	"time"
)

// Proxy is a reverse proxy with cool additional features
type Proxy struct {
	backendURL   *url.URL
	reverseProxy *httputil.ReverseProxy

	// Hold request signature of last visit of each client
	clientReqHash sync.Map
}

// NewProxy returns a new, initialized Proxy
func NewProxy(backendURL *url.URL) *Proxy {

	reverseProxy := httputil.NewSingleHostReverseProxy(backendURL)

	proxy := Proxy{
		backendURL:   backendURL,
		reverseProxy: reverseProxy,
	}

	return &proxy
}

// ServeHTTP handles requests to the proxy by intercepting the request,
// processing it and passing it along to the backend (if necessary)
func (p *Proxy) ServeHTTP(rw http.ResponseWriter, req *http.Request) {

	proxyRecorder := NewProxyRecorder(rw, req)
	var err error

	// Check for malicious code
	if isMalicious, err := p.isMalicious(req); err != nil {
		proxyRecorder.WriteHeader(http.StatusInternalServerError)
		proxyRecorder.Log()
		log.Printf("[ERROR] Error detecting malicious activity: %v\n", err)
		return
	} else if isMalicious {
		proxyRecorder.WriteHeader(http.StatusUnauthorized)
		proxyRecorder.Log()
		log.Printf("[WARN] Malicious activity detected from %s\n", req.RemoteAddr)
		return
	}

	// Delay duplicate requests
	proxyRecorder.wasDelayed, err = p.delayClient(req)
	if err != nil {
		proxyRecorder.WriteHeader(http.StatusInternalServerError)
		proxyRecorder.Log()
		log.Printf("[ERROR] Error delaying client: %v\n", err)
		return
	}

	// Request is good to pass onto the reverse proxy handler
	// TODO: capture and log the backend request duration
	proxyRecorder.RecordProxyTime()
	p.reverseProxy.ServeHTTP(proxyRecorder, req)
	proxyRecorder.Log()
}

// isMalicious returns true if the request is json and has a top-level JSON key of `is_malicious`
// Didn't want to rely on the content-type header as that can be manipulated, so we just read in the body
// and try to parse it
// TODO: Detect json without reading the whole body in
// TODO: Don't read whole body in (what if it's huge?)
func (p *Proxy) isMalicious(req *http.Request) (bool, error) {
	if req.Method == http.MethodPost {

		body, err := ioutil.ReadAll(req.Body)
		if err != nil {
			return false, err
		}

		// Try to unmarshal the json data structure
		c := make(map[string]json.RawMessage)
		err = json.Unmarshal(body, &c)

		// Not erroring on marshal failure here because not sure if non-json requests should be valid
		if err == nil {
			for s, _ := range c {
				if s == "is_malicious" {
					return true, nil
				}
			}
		}

		// We have to re-make the body reader for the backend since we closed the stream by reading it
		req.Body = ioutil.NopCloser(bytes.NewReader(body))
	}

	return false, nil
}

// delayClient delays subsequent requests from the same client (IP) that are exactly the same
// TODO: periodically clean up the clientReqHash (via background goroutine) so it doesn't grow forever
func (p *Proxy) delayClient(req *http.Request) (bool, error) {

	// Using RemoteAddr to uniquely identify clients (assuming no Proxies or LBs in front of this)
	// Other options based on infrstructure:
	// X-Forwarded-For
	// ProxyProtocol (v1/2)
	uniqueClientKey, _, err := net.SplitHostPort(req.RemoteAddr)
	if err != nil {
		return false, err
	}

	// Here we check if our client's request matches the previous request
	newHash, err := HashRequest(req)
	if err != nil {
		return false, err
	}

	lastHash, keyExists := p.clientReqHash.Load(uniqueClientKey)
	p.clientReqHash.Store(uniqueClientKey, newHash)

	// Delay if this request is the same as the last one
	isDelayed := false
	if keyExists {
		if newHash == lastHash {
			time.Sleep(2 * time.Second)
			isDelayed = true
		}
	}

	return isDelayed, nil
}

// HashRequest serializes the request and returns a computed a hash of the request
// Combines the headers, method, path, host and request body to form the hash
// Using MD5 because it is fairly fast.  CRC32 would be another good option
// Reference: https://blog.madewithdrew.com/post/benchmark-md5/
func HashRequest(req *http.Request) (string, error) {

	// strings.Builder is used to efficiently build a string using Write methods. It minimizes memory copying.
	var sb strings.Builder
	sb.WriteString(req.Host)
	sb.WriteString(req.Method)
	sb.WriteString(req.URL.String())

	// Since the Headers are stored in a map (unordered), we need to order them before serializing
	// so that we get the same hash for the same request
	HeaderKeys := make([]string, 0, len(req.Header))
	for k := range req.Header {
		HeaderKeys = append(HeaderKeys, k)
	}
	sort.Strings(HeaderKeys)
	for _, h := range HeaderKeys {
		sb.WriteString(h)
		for _, v := range req.Header[h] {
			sb.WriteString(v)
		}
	}

	body, err := ioutil.ReadAll(req.Body)
	if err != nil {
		return "", err
	}
	sb.Write(body)

	// We have to re-make the body reader for the backend since we closed the stream by reading it
	req.Body = ioutil.NopCloser(bytes.NewReader(body))

	hash := md5.Sum([]byte(sb.String()))
	return string(hash[:]), nil
}
