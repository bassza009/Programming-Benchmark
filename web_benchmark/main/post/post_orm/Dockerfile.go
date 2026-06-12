FROM golang:1.24-alpine

WORKDIR /app

RUN apk add --no-cache git

COPY go.mod .
COPY server.go .

RUN go mod tidy
RUN go build -o server server.go

EXPOSE 8004
CMD ["./server"]
