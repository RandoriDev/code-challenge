package main

import (
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"github.com/miguelapabenedit/dataArt-challange/docs"
	_ "github.com/miguelapabenedit/dataArt-challange/docs"
	"github.com/miguelapabenedit/dataArt-challange/package/controller"
	"github.com/miguelapabenedit/dataArt-challange/package/cors"
	httpSwagger "github.com/swaggo/http-swagger"
)

var (
	dataArtController        = controller.NewDataArtController()
	port              string = os.Getenv("PORT")
	host              string = os.Getenv("HOST")
)

// @title Data Art Challange
// @version 1.0
// @description This Api fowards Post request back to the client
// @contact.name API Support
// @contact.email miguell.beneditt@gmail.com
func main() {
	r := mux.NewRouter()
	handlePost := http.HandlerFunc(dataArtController.FowardRequest)

	r.Handle("/api", cors.Middleware(handlePost)).Methods(http.MethodPost)

	docs.SwaggerInfo.Host = host
	r.PathPrefix("/swagger").Handler(httpSwagger.WrapHandler)

	log.Printf("Running up on host:%s", host)
	log.Fatalln(http.ListenAndServe(":"+port, r))
}
