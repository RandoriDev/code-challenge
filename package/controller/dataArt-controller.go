package controller

import (
	"io/ioutil"
	"log"
	"net/http"
)

type controller struct {
}

/*NewDataArtController initialize a new controller*/
func NewDataArtController() Controller {
	return &controller{}
}

// FowardRequest godoc
// @Summary fowards the incoming request
// @ID foward-request
// @Description given a incoming request it fowards the message, if a key "is_malicous" is detected the request returns Unauthorized
// @Tags post
// @Accept json
// @Produce  json
// @Success 200
// @Param data body interface{} true "Data"
// @Failure 401 {string} string "Unauthorized"
// @Failure 500 {string} string "Internal Server error"
// @Router /api [post]
func (controller) FowardRequest(w http.ResponseWriter, r *http.Request) {
	bodyBytes, err := ioutil.ReadAll(r.Body)

	if err != nil {
		log.Println(err)
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	log.Println("Fowarding message to client.")
	w.Write(bodyBytes)
	return
}
