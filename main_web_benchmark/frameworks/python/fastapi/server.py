import os
import uuid
import asyncio
import logging
import multiprocessing
import aiomysql
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Disable verbose access logs during benchmarks
logging.getLogger("uvicorn.access").disabled = True
logging.getLogger("uvicorn").disabled = True

app = FastAPI()
pool = None

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

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    if pool:
        pool.close()
        await pool.wait_closed()

# ==================== Health Check ====================
@app.get("/")
async def root():
    return {"status": "success", "language": "Python", "framework": "FastAPI", "port": 8001}

# ==================== GET (Read) Endpoints ====================
@app.get("/raw/1table")
async def raw_1table():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM users LIMIT 100")
            return await cursor.fetchall()

@app.get("/raw/2join")
async def raw_2join():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "SELECT u.name, p.age FROM users u "
                "JOIN profiles p ON u.id = p.user_id LIMIT 100"
            )
            return await cursor.fetchall()

@app.get("/raw/3join")
async def raw_3join():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "SELECT u.name, p.age, o.total_amount FROM users u "
                "JOIN profiles p ON u.id = p.user_id "
                "JOIN orders o ON u.id = o.user_id LIMIT 100"
            )
            return await cursor.fetchall()

@app.get("/raw/4join")
async def raw_4join():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u "
                "JOIN profiles p ON u.id = p.user_id "
                "JOIN orders o ON u.id = o.user_id "
                "JOIN order_items oi ON o.id = oi.order_id LIMIT 100"
            )
            return await cursor.fetchall()

# ==================== POST (Write / Transaction) Endpoints ====================
@app.post("/raw/post/1table")
async def post_1table():
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                random_id = str(uuid.uuid4())[:8]
                email = f"py_{random_id}_{os.getpid()}_{id(cursor)}@example.com"
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
                email = f"py_{random_id}_{os.getpid()}_{id(cursor)}@example.com"
                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                user_id = cursor.lastrowid
                await cursor.execute(
                    "INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, 25, "123 Main St", f"Bio {user_id}", f"555-{random_id}")
                )
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
                email = f"py_{random_id}_{os.getpid()}_{id(cursor)}@example.com"
                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                user_id = cursor.lastrowid
                await cursor.execute(
                    "INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, 25, "123 Main St", f"Bio {user_id}", f"555-{random_id}")
                )
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
                email = f"py_{random_id}_{os.getpid()}_{id(cursor)}@example.com"
                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                user_id = cursor.lastrowid
                await cursor.execute(
                    "INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, 25, "123 Main St", f"Bio {user_id}", f"555-{random_id}")
                )
                await cursor.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)", (user_id, 100.00))
                order_id = cursor.lastrowid
                await cursor.execute(
                    "INSERT INTO order_items (order_id, product_name, price) VALUES (%s, %s, %s)",
                    (order_id, f"Item1_{random_id}", 25.00)
                )
                await cursor.execute(
                    "INSERT INTO order_items (order_id, product_name, price) VALUES (%s, %s, %s)",
                    (order_id, f"Item2_{random_id}", 75.00)
                )
                await conn.commit()
                return JSONResponse(status_code=201, content={"user_id": user_id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    workers = min(multiprocessing.cpu_count(), 8)
    uvicorn.run("server:app", host="0.0.0.0", port=8001, log_level="critical", workers=workers)
