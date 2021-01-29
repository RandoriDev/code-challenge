package domain

import (
	"bytes"
	"github.com/gin-gonic/gin"
	"github.com/santiagomoranlabat/da-api/config"
	"github.com/sirupsen/logrus"
	"io/ioutil"
	"sync"
	"time"
)

type request struct {
	lastSeen time.Time
	method   string
	path     string
	body     string
	headers  map[string][]string
}

var requests = make(map[string]*request)
var mu sync.Mutex

// init Run a background goroutine to remove old entries from the requests map.
func init() {
	go cleanupVisitors()
}

// BookRequestAndWait inspects that the last request is not equal, if doesn't exist or is different it creates or
// updates and stores it
func BookRequestAndWait(ip string, c *gin.Context) (error, bool) {
	var err error
	var wait bool
	mu.Lock()
	defer mu.Unlock()

	v, exists := requests[ip]
	if !exists {
		err = SetRequest(ip, c)
		return err, wait
	}

	isDuplicatedVisit, err := isDuplicatedRequest(ip, c)
	if err != nil {
		return err, wait
	}
	if isDuplicatedVisit {
		v.lastSeen = time.Now()
		wait = true
		return err, wait
	}

	// Has visited before, but has a new information and is going to be updated
	return SetRequest(ip, c), wait
}

// SetRequest save request with last seen using time.now()
func SetRequest(ip string, c *gin.Context) error {
	method := c.Request.Method
	headers := c.Request.Header
	path := c.Request.URL.Path
	body, err := ioutil.ReadAll(c.Request.Body)
	defer c.Request.Body.Close()
	c.Request.Body = ioutil.NopCloser(bytes.NewBuffer(body))
	if err != nil {
		logrus.Fatalf("Error reading Request Body, err: ", err)
		return err
	}

	requests[ip] = &request{
		time.Now(),
		method,
		path,
		string(body),
		headers,
	}

	return err
}

// isDuplicatedRequest compares the new request of gin.Context with the saved requests
func isDuplicatedRequest(ip string, c *gin.Context) (bool, error) {
	v, _ := requests[ip]

	// Compare method
	if v.method != c.Request.Method {
		return false, nil
	}

	// Compare path
	if v.path != c.Request.URL.Path {
		return false, nil
	}

	// Compare headers
	delete(v.headers, "X-Forwarded-For")
	if len(v.headers) != len(c.Request.Header) {
		return false, nil
	}
	for header := range v.headers {
		rh := c.Request.Header.Get(header)
		vh := v.headers[header][0]
		if rh != vh {
			return false, nil
		}
	}

	// Compare body
	body, err := ioutil.ReadAll(c.Request.Body)
	defer c.Request.Body.Close()
	c.Request.Body = ioutil.NopCloser(bytes.NewBuffer(body))
	if err != nil {
		logrus.Fatalf("Error reading Request Body, err: ", err)
		return false, err
	}
	if v.body != string(body) {
		return false, nil
	}

	return true, nil
}

// cleanupVisitors Every minute check the map for requests that haven't been seen for
// more than 10 minutes and delete the entries to flush the memory.
func cleanupVisitors() {
	for {
		time.Sleep(config.GetSamplingScheduleMinutes() * time.Minute)

		mu.Lock()
		for ip, v := range requests {
			if time.Since(v.lastSeen) > config.GetCleanupVisitorsExpirationMinutes() * time.Minute {
				delete(requests, ip)
			}
		}
		mu.Unlock()
	}
}

// DelayRequest delays by x seconds the request
func DelayRequest() {
	delayRequestTime := config.GetDelayRequestSeconds() * time.Second
	time.Sleep(delayRequestTime)
}
