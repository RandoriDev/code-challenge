package main

import (
	"log"
	"net/http"
)

func testHandler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte(`{ "name" : "backend_service", "value" : "Success" }`))
}

func main() {

	http.HandleFunc("/test", testHandler)
	log.Fatal(http.ListenAndServe(":3000", nil))
}
