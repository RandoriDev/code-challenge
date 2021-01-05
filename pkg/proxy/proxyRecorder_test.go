package proxy

import (
	"bytes"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"testing"
	"time"
)

type TestResponseWriter struct{}

func (rw TestResponseWriter) Write(buf []byte) (int, error) {
	return 0, nil
}

func (rw TestResponseWriter) WriteHeader(int) {}

func (rw TestResponseWriter) Header() http.Header {
	return nil
}

func TestProxyRecorder(t *testing.T) {

	rw := TestResponseWriter{}
	url, _ := url.Parse("http://foo.bar")
	req := http.Request{
		Method:     "PUT",
		URL:        url,
		RemoteAddr: "12.34.56.78",
		Header:     http.Header{"User-Agent": []string{"my-agent"}},
	}

	// Tests that the status gets captured correctly
	pr := NewProxyRecorder(rw, &req)
	pr.wasDelayed = true
	testStatus := 300
	pr.WriteHeader(testStatus)
	if pr.status != testStatus {
		t.Fatalf("Unexpected ProxyRecorder status: %d != %d", pr.status, testStatus)
	}

	// Test that the proxyduration gets recorded
	// Need to wait a tick to actually get some duration
	time.Sleep(20 * time.Microsecond)
	pr.RecordProxyTime()
	proxyDuration := pr.proxyDuration
	if proxyDuration <= 0 {
		t.Fatalf("ProxyRecorder duration not recorded")
	}

	// Redirect output to a buffer
	var buf bytes.Buffer
	log.SetOutput(&buf)
	defer func() {
		log.SetOutput(os.Stderr)
	}()

	// Ensure our log is in the expected format
	pr.Log()
	prLog := buf.String()
	prLog = prLog[20:] // Strip the timestamp off
	expectedLog := fmt.Sprintf("%s - [\"%s %s\" %s] %d %t [%d]\n", req.RemoteAddr, req.Method, req.URL.String(), req.UserAgent(), proxyDuration, pr.wasDelayed, pr.status)
	if prLog != expectedLog {
		t.Fatalf("ProxyRecorder log unexpected: '%s' != '%s'", prLog, expectedLog)
	}

}
