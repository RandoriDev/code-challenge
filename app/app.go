package app

import (
	"github.com/gin-gonic/gin"
	"github.com/santiagomoranlabat/da-api/config"
	"github.com/santiagomoranlabat/da-api/controller"
	"github.com/santiagomoranlabat/da-api/filter"
	"github.com/santiagomoranlabat/da-api/router"
	"os"
)

// Start starts the app, and inject the dependencies
func Start() *gin.Engine{
	handlers := injectDependencies()

	return start(handlers)
}

// start initialize the gin router and add the routes to handlers
func start(handler *router.Handlers) *gin.Engine {
	router := gin.Default()
	handler.MapRoutes(router)

	return router
}

// injectDependencies creates the handlers that are required by the app
func injectDependencies() *router.Handlers {
	handlers := &router.Handlers{
		PingController:         &controller.Ping{},
		ReverseProxyController: &controller.ReverseProxy{},
		MaliciousFilter:        &filter.Malicious{},
		DuplicatedFilter:       &filter.Duplicated{},
	}

	return handlers
}

// GetPortOrDefault tries to get the port from env or use default config
func GetPortOrDefault () string {
	port := os.Getenv("PORT")

	if port == "" {
		port = config.GetConfig().AppPort
	}

	return port
}
