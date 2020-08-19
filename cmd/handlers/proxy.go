package handlers

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"

	"go.uber.org/zap"
)

type ProxyHandler struct {
	target string

	client *http.Client
}

func NewProxyHandler(protocol, host string, port int) *ProxyHandler {
	h := ProxyHandler{
		target: fmt.Sprintf("%s://%s:%d", protocol, host, port),

		client: &http.Client{},
	}
	return &h
}

func (h *ProxyHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	logger := r.Context().Value("logger").(*zap.Logger)
	body := r.Context().Value("body").([]byte)

	fail := func(reason string, err error) {
		logger.Error("Request construction failed", zap.Error(err))
		http.Error(w, "Unable to proxy request", http.StatusInternalServerError)
	}

	url := fmt.Sprintf("%s%s", h.target, r.RequestURI)

	// Duplicate request data
	proxyRequest, err := http.NewRequest(r.Method, url, bytes.NewReader(body))
	if err != nil {
		fail("Request construction failed", err)
		return
	}
	proxyRequest.Header = r.Header
	// Add forwarding headers
	forwardedFor := strings.Trim(r.RemoteAddr[0:strings.LastIndex(r.RemoteAddr, ":")], "[]")
	proxyRequest.Header.Add("X-Forwarded-For", forwardedFor)
	proxyRequest.Header.Add("Forwarded", fmt.Sprintf("for=%s", forwardedFor))

	resp, err := h.client.Do(proxyRequest)
	if err != nil {
		fail("Proxied request failed", err)
		return
	}
	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fail("Proxied body unreadable", err)
		return
	}

	header := w.Header()
	for k, v := range resp.Header {
		header[k] = v
	}
	w.WriteHeader(resp.StatusCode)
	w.Write(b)
}
