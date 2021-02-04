package cors

import (
	"bytes"
	"encoding/json"
	"hash/fnv"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

var (
	mockCashe     = make(map[string]uint64)
	sleepTime int = 2
)

/*Middleware must be used to place logic and filters befor the service gets handler by the controller*/
func Middleware(handler http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Add("Access-Control-Allow-Origin", "*")
		w.Header().Add("Content-Type", "application/json")
		w.Header().Add("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")

		log.Println("Inspect for Spam started.")
		err := inspectSpamRequest(r)
		log.Println("Inspect for Spam completed.")

		if err != nil {
			log.Println(err)
			w.WriteHeader(http.StatusBadRequest)
			return
		}

		log.Println("Inspect for malicious content started.")
		var isMalicious bool
		if r.Method == http.MethodPost {
			isMalicious, err = inspectMaliciousRequest(r)
		}
		log.Println("Inspect for malicious content completed.")

		if err != nil {
			log.Println(err)
			w.WriteHeader(http.StatusBadRequest)
			return
		}

		if isMalicious {
			w.WriteHeader(http.StatusUnauthorized)
			return
		}

		handler.ServeHTTP(w, r)
	})
}

func inspectSpamRequest(r *http.Request) error {
	bodyBytes, err := ioutil.ReadAll(r.Body)
	defer restoreRequestBody(r, &bodyBytes)

	if err != nil {
		return err
	}

	bodyHash := getHash(&bodyBytes)
	clientIP := getClientIP(r)

	if val, ok := mockCashe[clientIP]; ok {
		if val == bodyHash {
			log.Printf("Spam detected from client:%s, aplying delay.", clientIP)
			time.Sleep(2 * time.Second)
		}
	}
	mockCashe[clientIP] = bodyHash

	return nil
}

func getHash(data *[]byte) uint64 {
	h := fnv.New64()
	h.Write(*data)
	return h.Sum64()
}

func inspectMaliciousRequest(r *http.Request) (bool, error) {
	var bodyData map[string]interface{}

	bodyBytes, err := ioutil.ReadAll(r.Body)
	defer restoreRequestBody(r, &bodyBytes)

	if err != nil {
		return false, err
	}

	err = json.Unmarshal(bodyBytes, &bodyData)
	if err != nil {
		return false, err
	}

	if _, ok := bodyData["is_malicious"]; ok {
		log.Println("A malicous content was detected.")
		return true, nil
	}

	log.Println("No malicous content detected.")
	return false, nil
}

func getClientIP(r *http.Request) string {
	clientIP := r.Header.Get("X-Real-Ip")

	if clientIP == "" {
		clientIP = r.Header.Get("X-Forwarded-For")
	}
	if clientIP == "" {
		clientIP = r.RemoteAddr
	}

	return clientIP
}

func restoreRequestBody(r *http.Request, rBoDY *[]byte) {
	r.Body = ioutil.NopCloser(bytes.NewBuffer(*rBoDY))
}
