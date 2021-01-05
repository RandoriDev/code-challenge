package main

import (
	"github.com/RandoriDev/code-challenge/pkg/proxy"
	"github.com/spf13/viper"
	"log"
	"net/http"
	"net/url"
)

func main() {
	rootCmd.Execute()
}

func startProxyServer() {
	listenAddr := viper.GetString("listen-addr")
	backendURL := viper.GetString("backend-url")

	if listenAddr == "" {
		log.Fatal("Must specify listener address for the proxy")
	}

	if backendURL == "" {
		log.Fatal("Must specify backend URL for the proxy")
	}

	proxyURL, err := url.Parse(backendURL)
	if err != nil {
		log.Fatalf("Error parsing backend address: %v", err)
	}

	log.Printf("Starting proxy server\n")
	log.Printf("Listening on %s\n", listenAddr)
	log.Printf("Forwarding to %s\n", backendURL)

	proxy := proxy.NewProxy(proxyURL)
	if err := http.ListenAndServe(listenAddr, proxy); err != nil {
		log.Fatalf("ListenAndServe: %v", err)
	}
}
