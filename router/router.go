package router

import (
	"github.com/gin-gonic/gin"
	"github.com/santiagomoranlabat/da-api/controller"
	"github.com/santiagomoranlabat/da-api/filter"
)

type Handlers struct {
	PingController         *controller.Ping
	ReverseProxyController *controller.ReverseProxy
	MaliciousFilter        *filter.Malicious
	DuplicatedFilter       *filter.Duplicated
}

// MapRoutes of the app specifying path and method
func (h *Handlers) MapRoutes(router *gin.Engine) {

	router.GET("/ping", h.PingController.GetOne)
	v1 := router.Group("/api/v1/da-api")
	v1.Use(h.DuplicatedFilter.Apply)

	v1.GET("/*da-api", h.ReverseProxyController.GetOne)
	v1.PUT("/*da-api", h.ReverseProxyController.GetOne)
	v1.PATCH("/*da-api", h.ReverseProxyController.GetOne)
	v1.HEAD("/*da-api", h.ReverseProxyController.GetOne)
	v1.OPTIONS("/*da-api", h.ReverseProxyController.GetOne)
	v1.DELETE("/*da-api", h.ReverseProxyController.GetOne)

	v1.POST("/*da-api", h.MaliciousFilter.Apply, h.ReverseProxyController.GetOne)
}
