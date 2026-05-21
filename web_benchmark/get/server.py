import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return JSONResponse(content={"status": "ok", "message": "Hello from Python GET Server", "language": "Python"})

@app.get("/health")
def read_health():
    return JSONResponse(content={"status": "healthy"})

@app.get("/api/data")
def read_data():
    return JSONResponse(content={"data": "benchmark_data", "timestamp": 1234567890, "value": 42})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    cpu_count = os.cpu_count() or 1
    workers = cpu_count * 2
    print(f"Python GET Server is running on port {port} with {workers} workers (cpu_count={cpu_count})")
    uvicorn.run("server:app", host="0.0.0.0", port=port, workers=workers, log_level="critical")
    