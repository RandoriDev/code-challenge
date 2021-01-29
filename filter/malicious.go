package filter

import (
	"bytes"
	"encoding/json"
	"github.com/gin-gonic/gin"
	"github.com/santiagomoranlabat/da-api/domain"
	"io/ioutil"
	"net/http"
	"github.com/sirupsen/logrus"
)

type Malicious struct{}

// Deny malicious request that has a key is_malicious in the body request
func (m *Malicious) Apply(c *gin.Context) {
	var malicious domain.Malicious
	body, err := ioutil.ReadAll(c.Request.Body)
	defer c.Request.Body.Close()
	if err != nil {
		logrus.Fatalf("Error reading Request Body, err: %s", err)
		return
	}
	c.Request.Body = ioutil.NopCloser(bytes.NewBuffer(body))
	err = json.Unmarshal(body, &malicious)
	if err != nil {
		logrus.Fatalf("Error filtering malicious condition, err: %v", err)
		c.String(http.StatusInternalServerError, "Internal error")
	}
	if malicious.IsMalicious {
		c.AbortWithStatus(http.StatusUnauthorized)
		return
	}

	c.Next()
}
