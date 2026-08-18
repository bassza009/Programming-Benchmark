# Node.js Fastify Benchmark Server

* **Language**: JavaScript / Node.js (v20+)
* **Framework**: Fastify
* **Database Driver**: `mysql2/promise` (Connection Pool)
* **Default Port**: `8002`

## Running Locally (Bare Metal)
```bash
npm install
npm start
```

## Running with Docker
```bash
docker build -t benchmark-fastify .
docker run -p 8002:8002 -e DB_HOST=host.docker.internal benchmark-fastify
```
