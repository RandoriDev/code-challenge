package controller

import "github.com/gin-gonic/gin"

type BaseController interface {
	GetOne(c *gin.Context)
}
