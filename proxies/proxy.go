package proxies

import "net/http"

type Proxy interface {

	// This method is intended to serve and intercept all the HTTP requests.
	ServeHTTP(writer http.ResponseWriter, req *http.Request)
}
