package filter

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/santiagomoranlabat/da-api/domain"
	"github.com/sirupsen/logrus"
	"net/http"
)

type Duplicated struct {}

// Allow Check for duplicated request, in case that found one waits 2 sec, and the continue the chain
func (d *Duplicated) Apply(c *gin.Context) {
	ip := c.ClientIP()

	err, wait := domain.BookRequestAndWait(ip, c)
	if err != nil {
		c.String(http.StatusBadRequest, fmt.Sprintf("Bad request, err: %v", err))
		c.Abort()
		return
	}
	if wait {
		domain.DelayRequest()
		logrus.Warnf("Request from: %s, method: %s is behind delayed. Duplicated request", ip, c.Request.Method)
	}

	c.Next()
}

