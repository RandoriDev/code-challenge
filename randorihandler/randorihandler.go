package randorihandler

import (
	"bytes"
	"crypto/sha1"
	"io/ioutil"
	"net/http"
	"sync"
	"time"

	"github.com/tidwall/gjson"
)

// The URL we're actually forwarding too
var backend string

// Holds how many messages we got
// thread safe
var rateLimiterQueue sync.Map

// Initialize all the things
func Initialize(backendURL string) {
	backend = backendURL
}

// SimpleHandler does the following
func SimpleHandler(w http.ResponseWriter, r *http.Request) {

	// Checking for only POST's
	switch r.Method {
	case http.MethodPost:

		defer r.Body.Close()

		// Reading the body
		rawData, err := ioutil.ReadAll(r.Body)

		if err != nil {
			http.Error(w, "Internal Server Error - Unable to parse `Body`", http.StatusInternalServerError)
			return
		}

		// Byte Array -> String
		data := string(rawData)

		// JSON Validation
		if !gjson.Valid(data) {
			http.Error(w, "Internal Server Error - `Body` is not valid JSON", http.StatusInternalServerError)
			return
		}

		// If it has the key `is_malicious` we should throw it out as Unauth
		isMalicious := gjson.Get(data, "is_malicious")
		if isMalicious.Exists() {
			http.Error(w, "401 Unauthorized - malicious", http.StatusUnauthorized)
			return
		}

		// Use a few of the parameters as a way to find dup requests
		// Use a SHA1 since it's small for a string size
		encodedBytes := sha1.Sum([]byte(r.Host + r.RemoteAddr + r.RequestURI + data))
		encoded := string(encodedBytes[:])

		// Using the sync Map, safely load or store 0 if it doesn't exist in our
		// rate limiter queue
		val, loaded := rateLimiterQueue.LoadOrStore(encoded, 0)
		if !loaded {
			newVal := val.(int)
			newVal++
			rateLimiterQueue.Store(encoded, newVal)
		}

		/*
			Originally `waitAndSend` was in a GoRoutine however, it became apparent that it was not needed
			and caused unwanted issues (panics!).

			For instance,
			   the HTTP Server is already running GoRoutines for each request that comes in
			   So the idea of having a Go Routine that `slept` for a few seconds was unneccessary
			   since you are already non-blocking to other requests.

			   the HTTP ResponseWrite can't leave this GoRoutine otherwise you'll
			   get panics from attempting to access it's internal channels that have already
			   gone out of scope and cleaned up

			   so, no `go` pleases

		*/
		waitAndSend(val.(int), encoded, w, r, rawData)

	default:
		http.Error(w, "Bad Request", http.StatusBadRequest)
	}
}

func waitAndSend(queueLength int, encoded string, w http.ResponseWriter, r *http.Request, rawData []byte) {

	// If we sent the requests to rapidly, hold up for a couple seconds...
	if queueLength > 1 {
		time.Sleep(2 * time.Second)
	}

	// You could use the same request, alter the URL that it's going too
	// but it is cleaner to make a new request with the appropriate information
	// from the original request
	proxyReq, err := http.NewRequest(r.Method, backend, bytes.NewReader(rawData))

	proxyReq.Header = r.Header
	proxyReq.Header.Set("X-Forwarded-Host", r.Header.Get("Host"))

	// Create a client
	httpClient := http.Client{}

	// Push the Request out
	resp, err := httpClient.Do(proxyReq)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	// Take the output from the backend request and throw it into
	// the response of the current requestor
	rawOutboundResult, err := ioutil.ReadAll(resp.Body)

	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}

	// Write the response
	w.Write(rawOutboundResult)

	// decrement the queue safely
	val, _ := rateLimiterQueue.Load(encoded)
	newVal, _ := val.(int)
	newVal--
	rateLimiterQueue.Store(encoded, newVal)
}
