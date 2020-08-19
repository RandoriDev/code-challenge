package handlers

import "net/http"

type NopHandler struct {
}

func NewNopHandler() *NopHandler {
	return &NopHandler{}
}

func (NopHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNoContent)
}
