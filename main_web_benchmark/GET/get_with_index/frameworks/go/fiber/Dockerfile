FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum* ./
RUN go mod download
COPY server.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o server server.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/server .
EXPOSE 8004
CMD ["./server"]
