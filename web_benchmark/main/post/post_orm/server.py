import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
import uvicorn

app = FastAPI()

# Database setup
DATABASE_URL = "mysql+aiomysql://admin:secret@127.0.0.1:3306/benchmark_db"
engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=10)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    bio = Column(String(255))
    phone = Column(String(20))

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    total_amount = Column(DECIMAL(10, 2))

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer)
    product_name = Column(String(100))
    price = Column(DECIMAL(10, 2))

def get_random_hex():
    return os.urandom(4).hex()

@app.post("/orm/post/1table")
async def post_1table():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            rand_id = get_random_hex()
            user = User(name=f"User_{rand_id}", email=f"test_{rand_id}@example.com")
            session.add(user)
            await session.flush()
            return {"user_id": user.id}

@app.post("/orm/post/2table")
async def post_2table():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            rand_id = get_random_hex()
            user = User(name=f"User_{rand_id}", email=f"test_{rand_id}@example.com")
            session.add(user)
            await session.flush()

            profile = Profile(user_id=user.id, bio=f"Bio for user {user.id}", phone=f"555-{rand_id}")
            session.add(profile)
            return {"user_id": user.id}

@app.post("/orm/post/3table")
async def post_3table():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            rand_id = get_random_hex()
            user = User(name=f"User_{rand_id}", email=f"test_{rand_id}@example.com")
            session.add(user)
            await session.flush()

            profile = Profile(user_id=user.id, bio=f"Bio for user {user.id}", phone=f"555-{rand_id}")
            order = Order(user_id=user.id, total_amount=100.00)
            session.add_all([profile, order])
            return {"user_id": user.id}

@app.post("/orm/post/4table")
async def post_4table():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            rand_id = get_random_hex()
            user = User(name=f"User_{rand_id}", email=f"test_{rand_id}@example.com")
            session.add(user)
            await session.flush()

            profile = Profile(user_id=user.id, bio=f"Bio for user {user.id}", phone=f"555-{rand_id}")
            order = Order(user_id=user.id, total_amount=100.00)
            session.add_all([profile, order])
            await session.flush()

            item1 = OrderItem(order_id=order.id, product_name=f"Product_{rand_id}_1", price=25.00)
            item2 = OrderItem(order_id=order.id, product_name=f"Product_{rand_id}_2", price=75.00)
            session.add_all([item1, item2])
            
            return {"user_id": user.id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="error")