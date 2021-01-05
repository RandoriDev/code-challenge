package proxy

import (
	"bufio"
	"bytes"
	"context"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
	"testing"
	"time"
)

// These are the values returned by the mock backend
const backendStatusCode = http.StatusOK
const backendCustomHeader = "X-Backend-Custom-Header"
const backendCustomHeaderValue = "foobar"
const backendResponse = "I am the backend"

// testProxyServer is a mock proxy/backend servers
type testProxyServer struct {
	frontend *httptest.Server
	backend  *httptest.Server
}

// request takes an http request and sends it to the proxy
func (p *testProxyServer) request(req *http.Request) (*http.Response, error) {
	client := p.frontend.Client()
	res, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	return res, nil
}

// start starts the mock backend server and mock proxy server
func (p *testProxyServer) start() {
	backend := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Add("X-Backend-Custom-Header", backendCustomHeaderValue)
		w.WriteHeader(backendStatusCode)
		w.Write([]byte(backendResponse))
	}))

	// Get the URL of the mock backend server
	backendURL, err := url.Parse(backend.URL)
	if err != nil {
		panic(err)
	}

	// Start the mock proxy server pointing to the mock backend
	proxy := NewProxy(backendURL)
	frontend := httptest.NewServer(proxy)

	p.backend = backend
	p.frontend = frontend
}

func newTestProxyServer() *testProxyServer {
	newTestProxyServer := &testProxyServer{}
	newTestProxyServer.start()
	return newTestProxyServer
}

// Tests the proxy's happy path
// Client request is passed through to the backend and response is passed back to the client
// TODO: Check to ensure the request recieved by the backend matches the request sent to the proxy
func TestProxyBasic(t *testing.T) {
	proxy := newTestProxyServer()
	req := newRequest(proxy.frontend.URL)
	res, err := proxy.request(req)
	if err != nil {
		t.Error(err)
	}

	// Ensure that the response we get is what we expect from the backend
	responseBody, err := ioutil.ReadAll(res.Body)
	if err != nil {
		t.Error(err)
	}

	assertEqualInt(t, res.StatusCode, backendStatusCode, "Backend response code unexpected")
	assertEqualString(t, res.Header.Get(backendCustomHeader), backendCustomHeaderValue, "Backend header did not return correctly")
	assertEqualString(t, string(responseBody), backendResponse, "Backend response body unexpected")
}

// Tests blocking of malicious content
// TODO: Ensure that the backend didn't recived the malicious response
func TestProxyMalicious(t *testing.T) {
	proxy := newTestProxyServer()
	body := `{"foo": "bar", "is_malicious": "most definitely"}`
	req, _ := http.NewRequest("POST", proxy.frontend.URL, bytes.NewBuffer([]byte(body)))

	res, err := proxy.request(req)
	if err != nil {
		t.Error(err)
	}

	assertEqualInt(t, res.StatusCode, http.StatusUnauthorized, "Malicious body didn't return correct status code")
}

// Tests throttling of duplicate requests
func TestProxyDuplicate(t *testing.T) {
	proxy := newTestProxyServer()
	req := newRequest(proxy.frontend.URL)

	// Ensure the initial request is quick (< 10ms)
	startTime := time.Now()
	_, err := proxy.request(req)
	if err != nil {
		t.Error(err)
	}
	elapsed := time.Since(startTime).Microseconds()
	if elapsed > 10000 {
		t.Fatalf("ProxyDuplicate: Initial request duration out of expected range: %d", elapsed)
	}

	// Ensure the second, duplicate request is delayed (between 2 and 2.01 seconds)
	startTime = time.Now()
	req = newRequest(proxy.frontend.URL)
	_, err = proxy.request(req)
	if err != nil {
		t.Error(err)
	}
	elapsed = time.Since(startTime).Microseconds()
	if elapsed < 2000000 || elapsed > 2010000 {
		t.Fatalf("ProxyDuplicate: Second (duplicate) request duration out of expected range: %d", elapsed)
	}

	// Ensure the third, non-duplicate request is fast (< 10ms)
	startTime = time.Now()
	req = newRequest(proxy.frontend.URL)
	req.Header["add"] = []string{"foo"}
	_, err = proxy.request(req)
	if err != nil {
		t.Error(err)
	}
	elapsed = time.Since(startTime).Microseconds()
	if elapsed > 10000 {
		t.Fatalf("ProxyDuplicate: Third (different) request duration out of expected range: %d", elapsed)
	}

}

// Reusable function for getting a baseline request
func newRequest(reqURL string) *http.Request {
	customHeader := "X-Custom-Header"
	customHeaderValue := "basic-test"
	customBody := "This is my request to the backend"
	req, _ := http.NewRequest("GET", reqURL, bytes.NewBuffer([]byte(customBody)))
	req.Host = "some-name"
	req.Header.Add(customHeader, customHeaderValue)
	return req
}

func assertEqualInt(t *testing.T, a interface{}, b interface{}, msg string) {
	if a != b {
		t.Fatalf("%s: %d != %d\n", msg, a, b)
	}
}

func assertEqualString(t *testing.T, a interface{}, b interface{}, msg string) {
	if a != b {
		t.Fatalf("%s: '%s' != '%s'\n", msg, a, b)
	}
}
