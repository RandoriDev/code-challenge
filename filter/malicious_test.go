package filter_test

import (
	"encoding/json"
	"github.com/santiagomoranlabat/da-api/app"
	"github.com/santiagomoranlabat/da-api/domain"
	"github.com/stretchr/testify/assert"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestMalicious_Deny(t *testing.T) {
	router := app.Start()
	maliciousJson := domain.Malicious{IsMalicious: true}
	byteMaliciousJson, _ := json.Marshal(maliciousJson)

	t.Run("Should deny a malicious POST json", func(t *testing.T) {
		req, _ := http.NewRequest("POST", "/api/v1/da-api/some/path", strings.NewReader(string(byteMaliciousJson)))
		resp := httptest.NewRecorder()
		router.ServeHTTP(resp, req)

		jsonResp, _ := ioutil.ReadAll(resp.Body)

		assert.Equal(t, http.StatusUnauthorized, resp.Code)
		assert.Equal(t, "", string(jsonResp))
	})
}
