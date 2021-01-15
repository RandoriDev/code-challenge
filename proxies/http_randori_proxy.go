package proxies

import (
	"crypto/md5"
	"encoding/json"
	cmap "github.com/orcaman/concurrent-map"
	log "github.com/sirupsen/logrus"
	"net/http"
	"net/http/httputil"
	"net/url"
	"time"
)

const (
	isMaliciousKey     = "is_malicious"
	timeForNextRequest = 2 * time.Second
)

// Implements the proxy interface
type randoriProxy struct {
	proxy          *httputil.ReverseProxy
	clientRequests cmap.ConcurrentMap
}

// Proxy designed to intersect the trafic and do the required validations
// before to send the request to the backend.
func NewRandoriProxy(url *url.URL) Proxy {
	return &randoriProxy{
		proxy:          httputil.NewSingleHostReverseProxy(url),
		clientRequests: cmap.New(),
	}
}

func (rp *randoriProxy) ServeHTTP(writer http.ResponseWriter, req *http.Request) {
	log.WithFields(log.Fields{
		"method": req.Method,
		"IP":     req.RemoteAddr,
		"Path":   req.URL.Path,
	}).Info("Request validation has started")
	var request map[string]interface{}
	decoder := json.NewDecoder(req.Body)
	if err := decoder.Decode(&request); err != nil {
		log.Info("Body could not be deserialized")
	}
	if req.Method == http.MethodPost && request[isMaliciousKey] != nil {
		log.WithFields(log.Fields{
			"method": req.Method,
			"IP":     req.RemoteAddr,
			"Path":   req.URL.Path,
			"Body":   request,
		}).Warn("Malicious request captured and rejected")
		writer.WriteHeader(http.StatusUnauthorized)
		return
	}

	rp.verifyLastRequestByClient(request, req)

	log.WithFields(log.Fields{
		"method": req.Method,
		"IP":     req.RemoteAddr,
		"Path":   req.URL.Path,
		"Body":   request,
	}).Debug("Request sent to the backend")
	rp.proxy.ServeHTTP(writer, req)
}

// This method verifies if a client, identified by the remoteAddress of the request, has sent the same request the
// last time if that's the case, the backend call will be delayed by a determined number of seconds.
func (rp *randoriProxy) verifyLastRequestByClient(request map[string]interface{}, req *http.Request) {
	clientIdentifier := req.RemoteAddr
	b, _ := json.Marshal(request)
	bodyStr := string(b)
	encodedBytes := md5.Sum([]byte(req.Method + bodyStr))

	lastRequest, ok := rp.clientRequests.Get(clientIdentifier)

	if ok && lastRequest == encodedBytes {
		log.WithFields(log.Fields{
			"IP": req.RemoteAddr,
		}).Info("Too many requests by client, delayed")
		rp.clientRequests.Remove(clientIdentifier)
		time.Sleep(timeForNextRequest)
	} else {
		rp.clientRequests.Set(clientIdentifier, encodedBytes)
	}
}
