# PHP Swoole Benchmark Server

* **Language**: PHP (8.2+)
* **Framework**: Swoole Engine (`PDOPool`)
* **Database Driver**: `PDO_MySQL` with Coroutines
* **Default Port**: `8003`

## Running Locally (Bare Metal)
```bash
php server.php
```

## Running with Docker
```bash
docker build -t benchmark-swoole .
docker run -p 8003:8003 -e DB_HOST=host.docker.internal benchmark-swoole
```
