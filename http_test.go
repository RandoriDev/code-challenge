package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/tidwall/gjson"
)

// TestLocalEndpoint ssss
func TestLocalEndpoint(t *testing.T) {

	// Setup the server with the following in main.go
	//r.Initialize("http://localhost:3000/test")

	var jsonStr = []byte(`{"title":"some random value"}`)
	req, err := http.NewRequest("POST", "http://localhost:8080/", bytes.NewBuffer(jsonStr))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("response Status:", resp.Status)
	fmt.Println("response Headers:", resp.Header)
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("response Body:", string(body))

	val := gjson.Get(string(body), "name")
	assert.Equal(t, val.String(), "backend_service", "JSON Value for `Name` was not the same")

	val = gjson.Get(string(body), "value")
	assert.Equal(t, val.String(), "Success", "JSON Value for `value` was not the same")
}

func TestLocalEndpointMalicious(t *testing.T) {

	// Setup the server with the following in main.go
	//r.Initialize("http://localhost:3000/test")

	var jsonStr = []byte(`{ "name" : "H4xx0r", "is_malicious" : "True" }`)
	req, err := http.NewRequest("POST", "http://localhost:8080/", bytes.NewBuffer(jsonStr))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	assert.Equal(t, resp.StatusCode, 401, "Is malicious, continuing on")
}
