cat <<EOF > Dockerfile.go
From golang:1.22-alpine
WORKDIR /app
COPY . .
RUN go build -o main benchmark/door/door.go
CMD ["./main"]
EOF
