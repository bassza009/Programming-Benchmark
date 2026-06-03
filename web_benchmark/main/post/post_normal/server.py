import aiomysql
import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import logging
import uuid

app = FastAPI()
pool = None

logging.getLogger("uvicorn.access").disabled = True
logging.getLogger("uvicorn").disabled = True

async def init_db():
    global pool
    pool = await aiomysql.create_pool(
        host='127.0.0.1',
        port=3306,
        user='admin',
        password='secret',
        db='benchmark_db',
        minsize=10,
        maxsize=100
    )

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
                    bio VARCHAR(255),
                    phone VARCHAR(20)
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
    return {"status": "success", "message": "Hello Benchmark"}

@app.post("/raw/post/1table")
async def post_1table():
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                random_id = str(uuid.uuid4())[:8]
                email = f"test_{random_id}@example.com"

                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                await conn.commit()

                user_id = cursor.lastrowid
                return JSONResponse(status_code=201, content={"user_id": user_id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/raw/post/2table")
async def post_2table():
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await conn.begin()

                random_id = str(uuid.uuid4())[:8]
                email = f"test_{random_id}@example.com"

                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                user_id = cursor.lastrowid

                await cursor.execute("INSERT INTO profiles (user_id, bio, phone) VALUES (%s, %s, %s)",
                                   (user_id, f"Bio for user {user_id}", f"555-{random_id}"))

                await conn.commit()
                return JSONResponse(status_code=201, content={"user_id": user_id})
    except Exception as e:
        try:
            await conn.rollback()
        except:
            pass
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/raw/post/3table")
async def post_3table():
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await conn.begin()

                random_id = str(uuid.uuid4())[:8]
                email = f"test_{random_id}@example.com"

                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                user_id = cursor.lastrowid

                await cursor.execute("INSERT INTO profiles (user_id, bio, phone) VALUES (%s, %s, %s)",
                                   (user_id, f"Bio for user {user_id}", f"555-{random_id}"))

                await cursor.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)",
                                   (user_id, 100.00))

                await conn.commit()
                return JSONResponse(status_code=201, content={"user_id": user_id})
    except Exception as e:
        try:
            await conn.rollback()
        except:
            pass
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/raw/post/4table")
async def post_4table():
    async with pool.acquire() as conn:
        try:
            async with conn.cursor() as cursor:
                await conn.begin()

                random_id = str(uuid.uuid4())[:8]
                email = f"test_{random_id}@example.com"

                await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
                user_id = cursor.lastrowid

                await cursor.execute("INSERT INTO profiles (user_id, bio, phone) VALUES (%s, %s, %s)",
                                   (user_id, f"Bio for user {user_id}", f"555-{random_id}"))

                await cursor.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)",
                                   (user_id, 100.00))
                order_id = cursor.lastrowid

                await cursor.execute("INSERT INTO order_items (order_id, product_name, price) VALUES (%s, %s, %s)",
                                   (order_id, f"Product_{random_id}_1", 25.00))
                await cursor.execute("INSERT INTO order_items (order_id, product_name, price) VALUES (%s, %s, %s)",
                                   (order_id, f"Product_{random_id}_2", 75.00))

                await conn.commit()
                return JSONResponse(status_code=201, content={"user_id": user_id})
                
        except Exception as e:
            await conn.rollback()
            return JSONResponse(status_code=500, content={"error": str(e)})
        
@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    import multiprocessing
    workers = multiprocessing.cpu_count() * 2
    uvicorn.run("server:app", host="0.0.0.0", port=8001, log_level="critical", workers=workers)
