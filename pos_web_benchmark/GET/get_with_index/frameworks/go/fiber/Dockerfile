FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY go.mod ./
RUN go mod download || true

COPY server.go ./
RUN go mod tidy && CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o server server.go

FROM alpine:3.19

WORKDIR /app
COPY --from=builder /app/server .

EXPOSE 8004

CMD ["./server"]
