import aiomysql
import asyncio
import warnings
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import logging

# ปิด Warning น่ารำคาญจาก aiomysql (เรื่อง Table already exists)
warnings.filterwarnings('ignore', module='aiomysql')
warnings.filterwarnings('ignore', category=Warning)

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
                    email VARCHAR(100)
                )
            """)

            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    age INT,
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

            await cursor.execute("SELECT COUNT(*) FROM users")
            count = await cursor.fetchone()

            if count[0] == 0:
                await insert_mock_data(conn, cursor)

            await conn.commit()

async def insert_mock_data(conn, cursor):
    for i in range(1, 10001):
        await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User{i}", f"user{i}@example.com"))
        await cursor.execute("INSERT INTO profiles (user_id, age, address) VALUES (%s, %s, %s)", (i, 20 + (i % 50), f"Address {i}"))
        await cursor.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)", (i, 100.0 + i))

        if i % 10 == 0:
            for j in range(5):
                await cursor.execute("INSERT INTO order_items (order_id, product_name, price) VALUES (%s, %s, %s)", (i, f"Product{j}", 10.0 + j))

    await conn.commit()

#เปลี่ยนมาใช้ระบบ lifespan แทน on_event (รองรับ FastAPI ตัวใหม่)
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    if pool:
        pool.close()
        await pool.wait_closed()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "success", "message": "Hello Benchmark"}

@app.get("/raw/1table")
async def raw_1table():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM users LIMIT 100")
            result = await cursor.fetchall()
            return result

@app.get("/raw/2join")
async def raw_2join():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT u.name, p.age FROM users u JOIN profiles p ON u.id = p.user_id LIMIT 100")
            result = await cursor.fetchall()
            return result

@app.get("/raw/3join")
async def raw_3join():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT u.name, p.age, o.total_amount FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id LIMIT 100")
            result = await cursor.fetchall()
            return result

@app.get("/raw/4join")
async def raw_4join():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id JOIN order_items oi ON o.id = oi.order_id LIMIT 100")
            result = await cursor.fetchall()
            return result

if __name__ == "__main__":
    import multiprocessing
    workers = multiprocessing.cpu_count() * 2
    
    print(f"server port 8001 amount {workers} Workers)...")
   
    
    # ถ้าอยากให้มี Log ขึ้น ให้เปลี่ยน "critical" เป็น "info" ครับ
    uvicorn.run("server:app", host="0.0.0.0", port=8001, log_level="critical", workers=workers)