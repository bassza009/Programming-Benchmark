FROM golang:1.21-alpine

WORKDIR /app
COPY server.go .

ENV PORT=8004
EXPOSE 8080

RUN go build -o server server.go

CMD ["./server"]
