package middleware

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/dambrisco/code-sample/pkg/cache"
	"go.uber.org/zap"
)

// Exampe of non-trivial middleware testing.
// Pattern can also be used to test handlers.
func TestThrottle(t *testing.T) {
	// Pick an arbitrary duration large enough to be noticeable
	delay := 1 * time.Second

	logger, err := zap.NewDevelopment()
	if err != nil {
		t.Fatal(err)
	}

	// Build the request and the necessary context.
	req, err := http.NewRequest("GET", "/", nil)
	if err != nil {
		t.Fatal(err)
	}
	req = req.WithContext(context.WithValue(req.Context(), "body", []byte{}))
	req = req.WithContext(context.WithValue(req.Context(), "logger", logger))

	rr := httptest.NewRecorder()
	handler := Throttle(cache.NewCache(), delay, http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write(nil)
	}))

	// TODO: Build a case array and use that instead

	// Test the first run.
	// If it takes more time than our delay, something's probably wrong.
	tStart := time.Now()
	handler.ServeHTTP(rr, req)
	if time.Since(tStart) > delay {
		t.Errorf("client appeared to be throttled on the first call")
	}

	// Test the second run.
	// If it takes less time than our delay, something's _definitely_ wrong.
	tStart = time.Now()
	handler.ServeHTTP(rr, req)
	if time.Since(tStart) < delay {
		t.Errorf("client appeared to not be throttled on the second call")
	}

	// Test the third run, but with a new method (should break caching).
	// If it takes more time than our delay, something's probably wrong.
	req.Method = "POST"
	tStart = time.Now()
	handler.ServeHTTP(rr, req)
	if time.Since(tStart) > delay {
		t.Errorf("client appeared to be throttled on the third call")
	}
}
