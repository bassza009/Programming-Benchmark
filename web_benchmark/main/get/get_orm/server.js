require("reflect-metadata");
const fastify = require("fastify")({ logger: false });
const { DataSource, EntitySchema } = require("typeorm");

const UserSchema = new EntitySchema({
  name: "User",
  tableName: "users",
  columns: {
    id: { primary: true, type: "int", generated: true },
    name: { type: "varchar", length: 100 },
    email: { type: "varchar", length: 100 }
  },
  relations: {
    profile: {
      type: "one-to-one",
      target: "Profile",
      inverseSide: "user",
      joinColumn: { name: "user_id" }
    },
    orders: {
      type: "one-to-many",
      target: "Order",
      inverseSide: "user"
    }
  }
});

const ProfileSchema = new EntitySchema({
  name: "Profile",
  tableName: "profiles",
  columns: {
    id: { primary: true, type: "int", generated: true },
    age: { type: "int" },
    address: { type: "varchar", length: 255 }
  },
  relations: {
    user: {
      type: "many-to-one",
      target: "User",
      joinColumn: { name: "user_id" },
      inverseSide: "profile"
    }
  }
});

const OrderSchema = new EntitySchema({
  name: "Order",
  tableName: "orders",
  columns: {
    id: { primary: true, type: "int", generated: true },
    total_amount: { type: "decimal", precision: 10, scale: 2 }
  },
  relations: {
    user: {
      type: "many-to-one",
      target: "User",
      joinColumn: { name: "user_id" },
      inverseSide: "orders"
    },
    orderItems: {
      type: "one-to-many",
      target: "OrderItem",
      inverseSide: "order"
    }
  }
});

const OrderItemSchema = new EntitySchema({
  name: "OrderItem",
  tableName: "order_items",
  columns: {
    id: { primary: true, type: "int", generated: true },
    product_name: { type: "varchar", length: 100 },
    price: { type: "decimal", precision: 10, scale: 2 }
  },
  relations: {
    order: {
      type: "many-to-one",
      target: "Order",
      joinColumn: { name: "order_id" },
      inverseSide: "orderItems"
    }
  }
});

const AppDataSource = new DataSource({
  type: "mysql",
  host: "127.0.0.1",
  port: 3306,
  username: "admin",
  password: "secret",
  database: "benchmark_db",
  synchronize: true,
  logging: false,
  entities: [UserSchema, ProfileSchema, OrderSchema, OrderItemSchema],
  extra: { connectionLimit: 100 }
});

async function insertMockData() {
  for (let i = 1; i <= 10000; i++) {
    await AppDataSource.query("INSERT INTO users (name, email) VALUES (?, ?)", [`User${i}`, `user${i}@example.com`]);
    await AppDataSource.query(
      "INSERT INTO profiles (user_id, age, address) VALUES (?, ?, ?)",
      [i, 20 + (i % 50), `Address ${i}`]
    );
    await AppDataSource.query("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", [i, 100.0 + i]);

    if (i % 10 === 0) {
      for (let j = 0; j < 5; j++) {
        await AppDataSource.query(
          "INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)",
          [i, `Product${j}`, 10.0 + j]
        );
      }
    }
  }
}

async function initDB() {
  await AppDataSource.initialize();
  const repository = AppDataSource.getRepository(UserSchema);
  const count = await repository.count();

  if (count === 0) {
    await insertMockData();
  }
}

fastify.get("/", async () => ({ status: "success", message: "Hello Benchmark" }));

fastify.get("/orm/1table", async () => {
  const repository = AppDataSource.getRepository(UserSchema);
  return repository.find({ take: 100 });
});

fastify.get("/orm/2join", async () => {
  return AppDataSource.getRepository(UserSchema)
    .createQueryBuilder("user")
    .select(["user.name AS name", "profile.age AS age"])
    .innerJoin("user.profile", "profile")
    .limit(100)
    .getRawMany();
});

fastify.get("/orm/3join", async () => {
  return AppDataSource.getRepository(UserSchema)
    .createQueryBuilder("user")
    .select(["user.name AS name", "profile.age AS age", "order.total_amount AS total_amount"])
    .innerJoin("user.profile", "profile")
    .innerJoin("user.orders", "order")
    .limit(100)
    .getRawMany();
});

fastify.get("/orm/4join", async () => {
  return AppDataSource.getRepository(UserSchema)
    .createQueryBuilder("user")
    .select([
      "user.name AS name",
      "profile.age AS age",
      "order.total_amount AS total_amount",
      "orderItem.product_name AS product_name"
    ])
    .innerJoin("user.profile", "profile")
    .innerJoin("user.orders", "order")
    .innerJoin("order.orderItems", "orderItem")
    .limit(100)
    .getRawMany();
});

initDB()
  .then(() => fastify.listen({ port: 8002, host: "0.0.0.0" }))
  .catch((err) => {
    console.error("Failed to initialize database:", err);
    process.exit(1);
  });
