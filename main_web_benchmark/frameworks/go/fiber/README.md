# Go Fiber Benchmark Server

* **Language**: Go (1.22+)
* **Framework**: Fiber (v2)
* **Database Driver**: `database/sql` + `go-sql-driver/mysql`
* **Default Port**: `8004`

## Running Locally (Bare Metal)
```bash
go run main.go
# or compile binary:
go build -o server main.go
./server
```

## Running with Docker
```bash
docker build -t benchmark-fiber .
docker run -p 8004:8004 -e DB_HOST=host.docker.internal benchmark-fiber
```
