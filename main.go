package main

import (
	"github.com/santiagomoranlabat/da-api/app"
	"github.com/sirupsen/logrus"
)

// main starts the app
func main() {
	proxy := app.Start()

	err := proxy.Run(app.GetPortOrDefault())
	if err != nil {
		logrus.Fatalf("Error starting the server. Error: %s", err)
	}
}
