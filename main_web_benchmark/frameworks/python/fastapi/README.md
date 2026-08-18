# Python FastAPI Benchmark Server

* **Language**: Python (3.11+)
* **Framework**: FastAPI + Uvicorn
* **Database Driver**: `aiomysql` (Async Connection Pool)
* **Default Port**: `8001`

## Running Locally (Bare Metal)
```bash
pip install -r requirements.txt
python server.py
```

## Running with Docker
```bash
docker build -t benchmark-fastapi .
docker run -p 8001:8001 -e DB_HOST=host.docker.internal benchmark-fastapi
```
