FROM golang:1.24-alpine

WORKDIR /app

RUN apk add --no-cache git

COPY server.go .
RUN go mod init benchmark && \
    go get github.com/gofiber/fiber/v2 && \
    go get github.com/go-sql-driver/mysql

RUN go build -o server server.go

EXPOSE 8004
CMD ["./server"]
