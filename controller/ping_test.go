package controller_test

import (
	"github.com/santiagomoranlabat/da-api/app"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestPing(t *testing.T) {
	router := app.Start()

	req, _ := http.NewRequest("GET", "/ping", nil)
	resp := httptest.NewRecorder()
	router.ServeHTTP(resp, req)

	jsonResp, _ := ioutil.ReadAll(resp.Body)

	assert.Equal(t, http.StatusOK, resp.Code)
	assert.Equal(t, "pong", string(jsonResp))
}
