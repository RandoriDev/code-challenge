package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

func main() {
	startClient()
}

func startClient() {
	var getMsg = `{ "ip": "10.168.01.01", "data": "Request message" }`
	var postMaliciousMsg = `{ "ip": "10.168.01.01", "data": "is_malicious:true" }`
	var postNonMaliciousMsg = `{ "ip": "10.168.01.01", "data": "is_none_malicious:true" }`

	httpRequest("GET", "http://localhost:8080", strings.NewReader(getMsg))
	httpRequest("GET", "http://localhost:8080", strings.NewReader(getMsg))
	httpRequest("POST", "http://localhost:8080", strings.NewReader(postMaliciousMsg))
	httpRequest("POST", "http://localhost:8080", strings.NewReader(postNonMaliciousMsg))

	var getMsg2 = `{ "ip": "10.168.01.02", "data": "Request message" }`
	var postMaliciousMsg2 = `{ "ip": "10.168.01.02", "data": "is_malicious:true" }`
	var postNonMaliciousMsg2 = `{ "ip": "10.168.01.02", "data": "is_none_malicious:true" }`

	httpRequest("GET", "http://localhost:8080", strings.NewReader(getMsg2))
	httpRequest("GET", "http://localhost:8080", strings.NewReader(getMsg2))
	httpRequest("POST", "http://localhost:8080", strings.NewReader(postMaliciousMsg2))
	httpRequest("POST", "http://localhost:8080", strings.NewReader(postNonMaliciousMsg2))

	select {}
}

func httpRequest(action, url string, msg *strings.Reader) {
	req, err := http.NewRequest(action, url, msg)

	if err != nil {
		fmt.Println(err)
	}

	req.Header.Set("Accept", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)

	if err != nil {
		fmt.Println(err)

		return
	}

	defer resp.Body.Close()

	bytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)

		return
	}

	fmt.Println("Response from Server: " + string(bytes))
}
