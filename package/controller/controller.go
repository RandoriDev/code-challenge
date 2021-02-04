package controller

import "net/http"

/*Controller interface represents the suported intents*/
type Controller interface {
	FowardRequest(w http.ResponseWriter, r *http.Request)
}
