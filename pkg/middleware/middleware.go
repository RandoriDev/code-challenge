package middleware

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"time"

	"github.com/dambrisco/code-sample/pkg/cache"
	"github.com/google/uuid"
	"go.uber.org/zap"
)

// Throttles duplicate requests based on a client's headers - ideally we'd
// identify the client via some auth scheme to track them more reliably.
// Context requires: "body":[]byte, "logger":*zap.Logger
func Throttle(cache *cache.Cache, delay time.Duration, next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		body := r.Context().Value("body").([]byte)
		logger := r.Context().Value("logger").(*zap.Logger)

		// We specify some components we need to dupe-check, but we'll let our caller
		// determine the requester's identity
		key := fmt.Sprintf("%v", r.Header)
		value := fmt.Sprintf("%s%s%s", r.Method, r.URL.String(), string(body))

		cache.Lock()
		defer cache.Unlock()
		// Update the timestamp to the current time regardless of result
		defer cache.Insert(key, value)
		if cache.Exists(key) && cache.Get(key) == value {
			logger.Debug("Client throttled",
				zap.Duration("duration", delay),
				zap.Any("header", r.Header))
			time.Sleep(delay)
		}
		next.ServeHTTP(w, r)
	})
}

// Finds and evaluates "is_malicious" keys at the top level of the body, if
// the body is a JSON object.
// Context requires: "body":[]byte, "logger":*zap.Logger
func Vet(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost {
			body := r.Context().Value("body").([]byte)
			logger := r.Context().Value("logger").(*zap.Logger)

			var j map[string]interface{}
			if err := json.Unmarshal(body, &j); err == nil {
				if val, ok := j["is_malicious"]; ok {
					if b, ok := val.(bool); ok && b {
						logger.Info("Malicous payload detected")
						http.Error(w, "Malicious payload detected", http.StatusUnauthorized)
						return
					}
				}
			}
		}
		next.ServeHTTP(w, r)
	})
}

// Logs out all received requests and relevant metadata.
// Context requires: "logger":*zap.Logger
func Log(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		body := r.Context().Value("pretty_body")
		logger := r.Context().Value("logger").(*zap.Logger)

		logger.Info("Request received",
			zap.String("proto", r.Proto),
			zap.String("method", r.Method),
			zap.String("remote_addr", r.RemoteAddr),
			zap.Any("header", r.Header),
			zap.Any("body", body))

		next.ServeHTTP(w, r)
	})
}

// Parses the body from context into JSON if possible.
// Context requires: "body":[]byte
func PrettyBody(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		body := r.Context().Value("body").([]byte)
		var i interface{}
		req := r
		if err := json.Unmarshal(body, &i); err == nil {
			req = r.WithContext(context.WithValue(r.Context(), "pretty_body", i))
		} else {
			req = r.WithContext(context.WithValue(r.Context(), "pretty_body", string(body)))
		}
		next.ServeHTTP(w, req)
	})
}

// Reads the request body into context and re-buffers it for any downstream
// consumers.
// Context requires: "logger":*zap.Logger
func Body(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		logger := r.Context().Value("logger").(*zap.Logger)
		// Risky - we should _really_ check and enforce content-length
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			logger.Error("Body unreadable", zap.Error(err))
			http.Error(w, "Body unreadable", http.StatusBadRequest)
			return
		}
		req := r.WithContext(context.WithValue(r.Context(), "body", body))
		req.Body = ioutil.NopCloser(bytes.NewBuffer(body))
		next.ServeHTTP(w, req)
	})
}

// Builds a logger for the request that includes the request ID with every call.
// Context requires: "request_id":string
func RequestLogger(logger *zap.Logger, next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		requestID := r.Context().Value("request_id").(string)
		requestLogger := logger.WithOptions(zap.Fields(zap.String("request_id", requestID)))
		req := r.WithContext(context.WithValue(r.Context(), "logger", requestLogger))
		next.ServeHTTP(w, req)
	})
}

// Generates a request ID and adds it to the context.
func Identify(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		requestID := uuid.New().String()
		req := r.WithContext(context.WithValue(r.Context(), "request_id", requestID))

		next.ServeHTTP(w, req)
	})
}
