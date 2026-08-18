import aiomysql
import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import logging
import os
import uuid

app = FastAPI()
pool = None

logging.getLogger("uvicorn.access").disabled = True
logging.getLogger("uvicorn").disabled = True

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "secret")
DB_NAME = os.getenv("DB_NAME", "benchmark_db")

async def init_db(retries=15):
    global pool
    for i in range(retries):
        try:
            pool = await aiomysql.create_pool(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASS,
                db=DB_NAME,
                minsize=5,
                maxsize=50,
                autocommit=True
            )
            break
        except Exception as e:
            if i == retries - 1:
                raise e
            await asyncio.sleep(1)

    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100) UNIQUE
                )
            """)

            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    age INT,
                    bio VARCHAR(255),
                    phone VARCHAR(20),
                    address VARCHAR(255)
                )
            """)

            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    total_amount DECIMAL(10, 2)
                )
            """)

            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT,
                    product_name VARCHAR(100),
                    price DECIMAL(10, 2)
                )
            """)

            await conn.commit()

@app.get("/")
async def root():
    return {"status": "success", "message": "Python FastAPI POST Benchmark"}

@app.post("/raw/post/1table")
async def post_1table():
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                random_id = str(uuid.uuid4())[:8]
                email = f"py_test_{random_id}_{os.getpid()}_{id(cursor)}@example.com"
                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                user_id = cursor.lastrowid
                return JSONResponse(status_code=201, content={"user_id": user_id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/raw/post/2table")
async def post_2table():
    try:
        async with pool.acquire() as conn:
            await conn.begin()
            async with conn.cursor() as cursor:
                random_id = str(uuid.uuid4())[:8]
                email = f"py_test_{random_id}_{os.getpid()}_{id(cursor)}@example.com"
                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                user_id = cursor.lastrowid
                await cursor.execute("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (%s, %s, %s, %s, %s)",
                                     (user_id, 25, "123 St", f"Bio {user_id}", f"555-{random_id}"))
                await conn.commit()
                return JSONResponse(status_code=201, content={"user_id": user_id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/raw/post/3table")
async def post_3table():
    try:
        async with pool.acquire() as conn:
            await conn.begin()
            async with conn.cursor() as cursor:
                random_id = str(uuid.uuid4())[:8]
                email = f"py_test_{random_id}_{os.getpid()}_{id(cursor)}@example.com"
                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                user_id = cursor.lastrowid
                await cursor.execute("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (%s, %s, %s, %s, %s)",
                                     (user_id, 25, "123 St", f"Bio {user_id}", f"555-{random_id}"))
                await cursor.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)", (user_id, 100.00))
                await conn.commit()
                return JSONResponse(status_code=201, content={"user_id": user_id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/raw/post/4table")
async def post_4table():
    try:
        async with pool.acquire() as conn:
            await conn.begin()
            async with conn.cursor() as cursor:
                random_id = str(uuid.uuid4())[:8]
                email = f"py_test_{random_id}_{os.getpid()}_{id(cursor)}@example.com"
                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                user_id = cursor.lastrowid
                await cursor.execute("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (%s, %s, %s, %s, %s)",
                                     (user_id, 25, "123 St", f"Bio {user_id}", f"555-{random_id}"))
                await cursor.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)", (user_id, 100.00))
                order_id = cursor.lastrowid
                await cursor.execute("INSERT INTO order_items (order_id, product_name, price) VALUES (%s, %s, %s)",
                                     (order_id, f"Prod1_{random_id}", 25.00))
                await cursor.execute("INSERT INTO order_items (order_id, product_name, price) VALUES (%s, %s, %s)",
                                     (order_id, f"Prod2_{random_id}", 75.00))
                await conn.commit()
                return JSONResponse(status_code=201, content={"user_id": user_id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    if pool:
        pool.close()
        await pool.wait_closed()

if __name__ == "__main__":
    import multiprocessing
    workers = min(multiprocessing.cpu_count(), 8)
    uvicorn.run("server:app", host="0.0.0.0", port=8001, log_level="critical", workers=workers)
