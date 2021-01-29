package controller

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

type Ping struct{}

const pong = "pong"

// GetOne ping with status 200 ok and text pong
func (h *Ping) GetOne(c *gin.Context) {
	c.String(http.StatusOK, pong)
}
