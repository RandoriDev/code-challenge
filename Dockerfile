FROM golang:1.15

COPY . /app
WORKDIR /app
ENV CGO_ENABLED=0

RUN ["go", "get", "github.com/githubnemo/CompileDaemon"]

ENTRYPOINT CompileDaemon -log-prefix=false -build="go build -o main -v /app/main.go" -command="./main"