ARG GO_VERSION=1.15.6

FROM golang:${GO_VERSION} AS dev
COPY . /src
WORKDIR /src/pkg/proxy
CMD ["go", "test", "-v"]

FROM golang:${GO_VERSION} AS build
WORKDIR /src
ENV CGO_ENABLED=0
COPY --from=dev /src /src
RUN go build -o /bin/proxy

FROM scratch
COPY --from=build /bin/proxy /bin/proxy
ENTRYPOINT ["/bin/proxy"]