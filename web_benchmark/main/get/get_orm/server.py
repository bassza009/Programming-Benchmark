import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, select, func, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, relationship
import uvicorn

DATABASE_URL = "mysql+aiomysql://admin:secret@127.0.0.1:3306/benchmark_db"

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100))
    profile = relationship("Profile", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    age = Column(Integer)
    address = Column(String(255))
    user = relationship("User", back_populates="profile")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Numeric(10, 2))
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_name = Column(String(100))
    price = Column(Numeric(10, 2))
    order = relationship("Order", back_populates="order_items")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=100,
    max_overflow=0,
    future=True,
)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        count = await session.scalar(select(func.count()).select_from(User))
        if count == 0:
            await insert_mock_data(session)
            await session.commit()

async def insert_mock_data(session: AsyncSession):
    for i in range(1, 10001):
        await session.execute(text(
            "INSERT INTO users (name, email) VALUES (:name, :email)"
        ), {"name": f"User{i}", "email": f"user{i}@example.com"})
        await session.execute(text(
            "INSERT INTO profiles (user_id, age, address) VALUES (:user_id, :age, :address)"
        ), {"user_id": i, "age": 20 + (i % 50), "address": f"Address {i}"})
        await session.execute(text(
            "INSERT INTO orders (user_id, total_amount) VALUES (:user_id, :total_amount)"
        ), {"user_id": i, "total_amount": 100.0 + i})

        if i % 10 == 0:
            for j in range(5):
                await session.execute(text(
                    "INSERT INTO order_items (order_id, product_name, price) VALUES (:order_id, :product_name, :price)"
                ), {"order_id": i, "product_name": f"Product{j}", "price": 10.0 + j})

        if i % 500 == 0:
            await session.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "success", "message": "Hello Benchmark"}

@app.get("/orm/1table")
async def orm_1table():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).limit(100))
        users = result.scalars().all()
        return [{"id": user.id, "name": user.name, "email": user.email} for user in users]

@app.get("/orm/2join")
async def orm_2join():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.name, Profile.age)
            .join(Profile, User.id == Profile.user_id)
            .limit(100)
        )
        return [{"name": row[0], "age": row[1]} for row in result.all()]

@app.get("/orm/3join")
async def orm_3join():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.name, Profile.age, Order.total_amount)
            .join(Profile, User.id == Profile.user_id)
            .join(Order, User.id == Order.user_id)
            .limit(100)
        )
        return [{"name": row[0], "age": row[1], "total_amount": float(row[2])} for row in result.all()]

@app.get("/orm/4join")
async def orm_4join():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.name, Profile.age, Order.total_amount, OrderItem.product_name)
            .join(Profile, User.id == Profile.user_id)
            .join(Order, User.id == Order.user_id)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .limit(100)
        )
        return [
            {
                "name": row[0],
                "age": row[1],
                "total_amount": float(row[2]),
                "product_name": row[3],
            }
            for row in result.all()
        ]

if __name__ == "__main__":
    import multiprocessing

    workers = multiprocessing.cpu_count() * 2
    uvicorn.run("server:app", host="0.0.0.0", port=8001, log_level="critical", workers=workers)
