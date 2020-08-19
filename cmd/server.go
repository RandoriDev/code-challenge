package main

import (
	"errors"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/dambrisco/code-sample/cmd/handlers"
	"github.com/dambrisco/code-sample/pkg/cache"
	"github.com/dambrisco/code-sample/pkg/middleware"
	"github.com/spf13/viper"
	"go.uber.org/zap"
)

func main() {
	term := make(chan os.Signal, 1)
	signal.Notify(term, os.Interrupt, syscall.SIGTERM)

	viper.SetEnvPrefix("sample")
	viper.AutomaticEnv()

	// Load configuration
	port := viper.GetInt("port")
	delay := time.Duration(viper.GetInt("delay_ms")) * time.Millisecond
	targetProtocol := viper.GetString("target_protocol")
	targetHost := viper.GetString("target_host")
	targetPort := viper.GetInt("target_port")
	mockBackend := viper.GetBool("mock_backend")

	// Build dependencies
	// TODO: Ideally we'd use DI for this, but that's _definitely_ overkill here.
	cache := cache.NewCache()
	logger, err := zap.NewDevelopment()
	if err != nil {
		panic(err)
	}
	defer logger.Sync()

	proxyHandler := handlers.NewProxyHandler(targetProtocol, targetHost, targetPort)

	proxyServer := http.Server{
		Addr: fmt.Sprintf(":%d", port),
		// TODO: Use collections of middleware instead of wrapping directly.
		Handler: middleware.Identify(
			middleware.RequestLogger(logger,
				middleware.Body(
					middleware.PrettyBody(
						middleware.Log(
							middleware.Vet(
								middleware.Throttle(cache, delay, proxyHandler))))))),
	}
	defer proxyServer.Close()

	serverError := make(chan error, 1)
	go serve(&proxyServer, serverError)
	logger.Info("Serving proxy", zap.Int("port", port))

	// In an actual implementation, we probably shouldn't include this at all.
	if mockBackend {
		backendHandler := handlers.NewNopHandler()
		backendServer := http.Server{
			Addr:    fmt.Sprintf(":%d", targetPort),
			Handler: backendHandler,
		}
		defer backendServer.Close()
		go serve(&backendServer, serverError)
		logger.Info("Serving mock backend", zap.Int("port", targetPort))
	}

	var fatal error
	select {
	case fatal = <-serverError:
	case <-term:
		fatal = errors.New("Interrupt received")
	}
	logger.Error("Server shutting down", zap.Error(fatal))
}

func serve(server *http.Server, err chan error) {
	err <- server.ListenAndServe()
}
