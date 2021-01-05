package proxy

import (
	"log"
	"net/http"
	"time"
)

// ProxyRecorder records and log requests and responses from a proxy server
type ProxyRecorder struct {
	http.ResponseWriter
	request       *http.Request
	status        int
	wasDelayed    bool
	startTime     time.Time
	proxyDuration int64 // Duration in microseconds
}

// NewProxyRecorder creates a new ProxyRecorder
// Also starts a timer that can be ended with RecordProxyTime()
func NewProxyRecorder(rw http.ResponseWriter, req *http.Request) *ProxyRecorder {
	pr := ProxyRecorder{
		ResponseWriter: rw,
		request:        req,
		startTime:      time.Now(),
	}
	return &pr
}

// WriteHeader hijacks the WriteHeader() method of the http.ResponseWriter to capture the returned status code
// https://golang.org/pkg/net/http/#ResponseWriter
func (pr *ProxyRecorder) WriteHeader(status int) {
	pr.status = status
	pr.ResponseWriter.WriteHeader(status)
}

// RecordProxyTime stop the timer for recording the proxy request duration
// TODO: Make this more reusable to record different parts of the request
func (pr *ProxyRecorder) RecordProxyTime() {
	pr.proxyDuration = time.Since(pr.startTime).Microseconds()
}

// Log prints the proxy request details
// TODO: Make format configurable
func (pr *ProxyRecorder) Log() {
	log.Printf("%s - [\"%s %s\" %s] %d %t [%d]\n", pr.request.RemoteAddr, pr.request.Method, pr.request.URL.String(), pr.request.UserAgent(), pr.proxyDuration, pr.wasDelayed, pr.status)
}
