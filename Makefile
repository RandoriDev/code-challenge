PORT?=8080
TARGET_PROTOCOL?=http
TARGET_HOST?=localhost
TARGET_PORT?=8081
DELAY_MS?=2000

vet:
	go vet ./...

test: vet
	go test ./...

build: vet
	go build -o bin/server cmd/server.go

run: build
	@SAMPLE_PORT=$(PORT) \
		SAMPLE_TARGET_PROTOCOL=$(TARGET_PROTOCOL) \
		SAMPLE_TARGET_HOST=$(TARGET_HOST) \
		SAMPLE_TARGET_PORT=$(TARGET_PORT) \
		SAMPLE_DELAY_MS=$(DELAY_MS) \
		SAMPLE_MOCK_BACKEND=1 \
		./bin/server
