From golang:1.22-alpine
WORKDIR /app
COPY . .
RUN go build -o main door.go
RUN go build -o mainnprint doorNoprint.go

