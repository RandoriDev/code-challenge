package main

import (
	"log"
	"net/http"

	r "randori.com/amerrill/randorihandler"
)

func main() {
	r.Initialize("http://localhost:3000/test")

	// If you Init with the following, and pass "{}" as the JSON, you do hit their API
	//r.Initialize("https://jsonplaceholder.typicode.com/posts")
	http.HandleFunc("/", r.SimpleHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
