package proxies

import (
	"bytes"
	"github.com/stretchr/testify/assert"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"net/url"
	"testing"
	"time"
)

const (
	backendResponse = "someResponse"
)

func initBackendServer() *httptest.Server {
	backend := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Randori", "security")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(backendResponse))
	}))
	return backend
}

func TestRandoriProxy_ServeHTTP_Success(t *testing.T) {
	backend := initBackendServer()
	defer backend.Close()
	backendURL, err := url.Parse(backend.URL)
	if err != nil {
		t.Fatal(err)
	}
	proxyHandler := NewRandoriProxy(backendURL)
	frontend := httptest.NewServer(proxyHandler)
	defer frontend.Close()
	frontendClient := frontend.Client()

	getReq, _ := http.NewRequest("POST", frontend.URL, nil)
	getReq.Host = "some-name"
	getReq.Close = true
	res, err := frontendClient.Do(getReq)

	bodyBytes, _ := ioutil.ReadAll(res.Body)
	assert.Equal(t, http.StatusOK, res.StatusCode)
	assert.Equal(t, "security", res.Header.Get("Randori"))
	assert.Equal(t, backendResponse, string(bodyBytes))
}

func TestRandoriProxy_ServeHTTP_BadGateway(t *testing.T) {
	backendURL, err := url.Parse("http://localhost:8081")
	if err != nil {
		t.Fatal(err)
	}
	proxyHandler := NewRandoriProxy(backendURL)
	frontend := httptest.NewServer(proxyHandler)
	defer frontend.Close()
	frontendClient := frontend.Client()

	getReq, _ := http.NewRequest("POST", frontend.URL+"/invalidPath", nil)
	getReq.Host = "some-name"
	getReq.Close = true
	res, _ := frontendClient.Do(getReq)

	assert.Equal(t, http.StatusBadGateway, res.StatusCode)
}

func TestRandoriProxy_ServeHTTP_Unautorized(t *testing.T) {
	backend := initBackendServer()
	defer backend.Close()
	backendURL, err := url.Parse(backend.URL)
	if err != nil {
		t.Fatal(err)
	}
	proxyHandler := NewRandoriProxy(backendURL)
	frontend := httptest.NewServer(proxyHandler)
	defer frontend.Close()
	frontendClient := frontend.Client()

	body := bytes.NewBuffer([]byte(`{"is_malicious": true}`))
	getReq, _ := http.NewRequest("POST", frontend.URL, body)
	getReq.Host = "some-name"
	getReq.Close = true
	res, err := frontendClient.Do(getReq)

	assert.Equal(t, http.StatusUnauthorized, res.StatusCode)
}

func TestRandoriProxy_ServeHTTP_DelayTwoSeconds(t *testing.T) {
	startTime := time.Now()
	backend := initBackendServer()
	defer backend.Close()
	backendURL, err := url.Parse(backend.URL)
	if err != nil {
		t.Fatal(err)
	}

	proxyHandler := NewRandoriProxy(backendURL)
	frontend := httptest.NewServer(proxyHandler)
	defer frontend.Close()
	frontendClient := frontend.Client()

	getReq, _ := http.NewRequest("POST", frontend.URL, nil)
	getReq.Host = "0.0.0.0"
	getReq.Close = true
	res, err := frontendClient.Do(getReq)

	getReq, _ = http.NewRequest("POST", frontend.URL, nil)
	getReq.Host = "0.0.0.0"
	getReq.Close = true
	res, err = frontendClient.Do(getReq)

	bodyBytes, _ := ioutil.ReadAll(res.Body)
	assert.Equal(t, http.StatusOK, res.StatusCode)
	assert.Equal(t, "security", res.Header.Get("Randori"))
	assert.Equal(t, backendResponse, string(bodyBytes))
	assert.True(t, time.Since(startTime) > 20000)
}
