From golang:1.22-alpine
WORKDIR /app
COPY . .
RUN go build -o main Metrix.go
RUN go build -o main2 Metrixv2.go

