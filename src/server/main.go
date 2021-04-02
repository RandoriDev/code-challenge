package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"
	"time"

	"server/clientshandler"
	"server/logger"
	"server/processor"
)

var clientHandler clientshandler.Object
var log logger.Object
var proc processor.Object

func main() {
	http.HandleFunc("/", ProcessHttpRequests)

	clientHandler.Start()
	log.Start()
	proc.Start()

	listeningMsg := "Listening at port 8080\n"

	log.LogToFile(listeningMsg)
	fmt.Println(listeningMsg)

	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println(err)
	}

	select {}
}

func ProcessHttpRequests(w http.ResponseWriter, r *http.Request) {
	b, err := ioutil.ReadAll(r.Body)
	defer r.Body.Close()

	if err != nil {
		log.LogToFile(err.Error())
		return
	}

	var msg processor.Request
	err = json.Unmarshal(b, &msg)
	if err != nil {
		log.LogToFile(err.Error())
		return
	}

	delay := clientHandler.ShouldDelay(msg.Ip, msg.Data)

	if delay {
		time.Sleep(2 * time.Second)
	}

	msg.RequestDelayed = delay

	var outStr = ""
	requestChannel := make(chan processor.Request)

	switch r.Method {
	case "GET":
		proc.Channel <- requestChannel
		requestChannel <- msg
		res := <-requestChannel

		out, err := json.Marshal(res)

		if err != nil {
			fmt.Fprintf(w, err.Error(), http.StatusInternalServerError)

			return
		}

		outStr = "GET Response: \t" + string(out)

		log.LogToFile(outStr)
		fmt.Fprintf(w, outStr)
	case "POST":
		if strings.Contains(msg.Data, "is_malicious") {
			msg.ServerInformation = processor.Server{
				Time:     time.Now(),
				HttpCode: http.StatusUnauthorized,
				Details:  "Request not authorized",
			}

			out, err := json.Marshal(msg)

			if err != nil {
				fmt.Fprintf(w, err.Error(), http.StatusInternalServerError)

				return
			}

			outStr = "POST Response: \t" + string(out)

			log.LogToFile(outStr)
			fmt.Fprintf(w, outStr)

			return
		}

		proc.Channel <- requestChannel
		requestChannel <- msg

		res := <-requestChannel

		out, err := json.Marshal(res)

		if err != nil {
			fmt.Fprintf(w, err.Error(), http.StatusInternalServerError)

			return
		}

		outStr = "POST Response: \t" + string(out)

		log.LogToFile(outStr)
		fmt.Fprintf(w, outStr)
	default:
		outStr = "Sorry, only GET and POST methods are supported. Http Code: " + strconv.Itoa(http.StatusNotFound)

		log.LogToFile(outStr)
		fmt.Fprintf(w, outStr)
	}
}
