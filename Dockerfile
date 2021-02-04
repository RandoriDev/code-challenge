FROM golang:latest

WORKDIR /app

COPY go.mod ./go.mod  
COPY go.sum ./go.sum 

RUN go mod download
COPY . .

ENV PORT=5000
ENV HOST="localhost:5000"

RUN go build ./main.go

CMD ["./main"]