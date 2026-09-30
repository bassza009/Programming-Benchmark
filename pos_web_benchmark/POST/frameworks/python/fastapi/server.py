import os
import asyncio
import uuid
import time
from fastapi import FastAPI, HTTPException
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
    return {"status": "success", "message": "Python FastAPI PostgreSQL POST Benchmark"}

@app.post("/raw/post/1table", status_code=201)
async def post_1table():
    uid = uuid.uuid4().hex[:8]
    email = f"user_{uid}_{time.time_ns()}@example.com"
    async with pool.acquire() as conn:
        customer_id = await conn.fetchval(
            "INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id",
            f"Customer_{uid}", email, f"555-{uid}", "Benchmark City"
        )
        return {"customer_id": customer_id}

@app.post("/raw/post/2table", status_code=201)
async def post_2table():
    uid = uuid.uuid4().hex[:8]
    email = f"user_{uid}_{time.time_ns()}@example.com"
    async with pool.acquire() as conn:
        async with conn.transaction():
            customer_id = await conn.fetchval(
                "INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id",
                f"Customer_{uid}", email, f"555-{uid}", "Benchmark City"
            )
            order_id = await conn.fetchval(
                "INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES ($1, $2, $3, $4, $5) RETURNING id",
                customer_id, 1, 2, 150.00, "COMPLETED"
            )
            return {"customer_id": customer_id, "order_id": order_id}

@app.post("/raw/post/3table", status_code=201)
async def post_3table():
    uid = uuid.uuid4().hex[:8]
    email = f"user_{uid}_{time.time_ns()}@example.com"
    async with pool.acquire() as conn:
        async with conn.transaction():
            customer_id = await conn.fetchval(
                "INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id",
                f"Customer_{uid}", email, f"555-{uid}", "Benchmark City"
            )
            product_id = await conn.fetchval(
                "INSERT INTO product (factory_id, name, category, price, stock) VALUES ($1, $2, $3, $4, $5) RETURNING id",
                1, f"Product_{uid}", "Benchmark Category", 99.99, 100
            )
            order_id = await conn.fetchval(
                "INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES ($1, $2, $3, $4, $5) RETURNING id",
                customer_id, product_id, 1, 99.99, "COMPLETED"
            )
            return {"customer_id": customer_id, "product_id": product_id, "order_id": order_id}

@app.post("/raw/post/4table", status_code=201)
async def post_4table():
    uid = uuid.uuid4().hex[:8]
    email = f"user_{uid}_{time.time_ns()}@example.com"
    async with pool.acquire() as conn:
        async with conn.transaction():
            factory_id = await conn.fetchval(
                "INSERT INTO factory (name, location, country) VALUES ($1, $2, $3) RETURNING id",
                f"Factory_{uid}", "Industrial Estate", "Thailand"
            )
            product_id = await conn.fetchval(
                "INSERT INTO product (factory_id, name, category, price, stock) VALUES ($1, $2, $3, $4, $5) RETURNING id",
                factory_id, f"Product_{uid}", "Benchmark Category", 99.99, 100
            )
            customer_id = await conn.fetchval(
                "INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id",
                f"Customer_{uid}", email, f"555-{uid}", "Benchmark City"
            )
            order_id = await conn.fetchval(
                "INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES ($1, $2, $3, $4, $5) RETURNING id",
                customer_id, product_id, 1, 99.99, "COMPLETED"
            )
            return {"factory_id": factory_id, "product_id": product_id, "customer_id": customer_id, "order_id": order_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001, access_log=False)
