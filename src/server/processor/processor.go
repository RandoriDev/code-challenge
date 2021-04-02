package processor

import (
	"net/http"
	"time"
)

type Object struct {
	Channel chan chan Request
}

type Request struct {
	Ip                string `json:"ip"`
	Data              string `json:"data"`
	RequestDelayed    bool
	ServerInformation Server
}

type Server struct {
	Time              time.Time
	HttpCode          int
	ProcessedByServer bool
	Details           string
}

func (p *Object) Start() {
	p.Channel = make(chan chan Request, 100)

	go func() {
		for {
			select {
			case ch := <-p.Channel:
				go func() {
					for {
						select {
						case req := <-ch:
							req.ServerInformation = Server{
								Time:              time.Now(),
								HttpCode:          http.StatusOK,
								ProcessedByServer: true,
								Details:           "Processed by server successfully",
							}

							ch <- req
						default:
							//fmt.Println("No Request received yet")
						}
					}
				}()
			default:
				//fmt.Println("No Channel received yet")
			}
		}
	}()
}
