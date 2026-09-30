import os
import asyncio
from fastapi import FastAPI
import asyncpg
from contextlib import asynccontextmanager

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "secret")
DB_NAME = os.getenv("DB_NAME", "benchmark_db")

pool: asyncpg.Pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    max_retries = 30
    for i in range(max_retries):
        try:
            pool = await asyncpg.create_pool(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                min_size=20,
                max_size=100,
                max_inactive_connection_lifetime=300.0,
                command_timeout=30.0
            )
            break
        except Exception as e:
            if i == max_retries - 1:
                raise e
            await asyncio.sleep(1)
    yield
    if pool:
        await pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "success", "message": "Python FastAPI PostgreSQL GET Benchmark"}

@app.get("/raw/1table")
async def raw_1table():
    async with pool.acquire() as conn:
        records = await conn.fetch("SELECT id, name, email, phone, city, created_at FROM customer LIMIT 100")
        return [dict(r) for r in records]

@app.get("/raw/2join")
async def raw_2join():
    async with pool.acquire() as conn:
        records = await conn.fetch("""
            SELECT o.id, c.name, o.quantity, o.total_amount, o.order_date
            FROM orders o
            JOIN customer c ON o.customer_id = c.id
            LIMIT 100
        """)
        return [dict(r) for r in records]

@app.get("/raw/3join")
async def raw_3join():
    async with pool.acquire() as conn:
        records = await conn.fetch("""
            SELECT o.id, c.name, p.name AS product_name, o.quantity, o.total_amount
            FROM orders o
            JOIN customer c ON o.customer_id = c.id
            JOIN product p ON o.product_id = p.id
            LIMIT 100
        """)
        return [dict(r) for r in records]

@app.get("/raw/4join")
async def raw_4join():
    async with pool.acquire() as conn:
        records = await conn.fetch("""
            SELECT o.id, c.name, p.name AS product_name, f.name AS factory_name, o.quantity, o.total_amount
            FROM orders o
            JOIN customer c ON o.customer_id = c.id
            JOIN product p ON o.product_id = p.id
            JOIN factory f ON p.factory_id = f.id
            LIMIT 100
        """)
        return [dict(r) for r in records]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001, access_log=False)
