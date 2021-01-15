package main

import (
	"code-challenge/proxies"
	log "github.com/sirupsen/logrus"
	"net/http"
	"net/url"
	"os"
)

func init() {
	// Here all the logging setup
	log.SetFormatter(&log.JSONFormatter{})

	file, err := os.OpenFile("logrus.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err == nil {
		log.SetOutput(file)
	} else {
		log.Info("Failed to log to file, using default stderr")
	}

	log.SetLevel(log.InfoLevel)
}

func main() {
	target := os.Getenv("BACKEND_URL")
	proxyUrl, _ := url.Parse(target)
	randoriProxy := proxies.NewRandoriProxy(proxyUrl)

	if err := http.ListenAndServe(":"+os.Getenv("PROXY_PORT"), randoriProxy); err != nil {
		panic(err)
	}
}
