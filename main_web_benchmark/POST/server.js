const fastify = require('fastify');
const mysql = require('mysql2/promise');
const crypto = require('crypto');

const app = fastify({ logger: false });
let pool;

const DB_HOST = process.env.DB_HOST || '127.0.0.1';
const DB_PORT = parseInt(process.env.DB_PORT || '3306');
const DB_USER = process.env.DB_USER || 'admin';
const DB_PASS = process.env.DB_PASS || 'secret';
const DB_NAME = process.env.DB_NAME || 'benchmark_db';

async function initDB() {
  pool = await mysql.createPool({
    host: DB_HOST,
    port: DB_PORT,
    user: DB_USER,
    password: DB_PASS,
    database: DB_NAME,
    waitForConnections: true,
    connectionLimit: 100,
    queueLimit: 0
  });

  const connection = await pool.getConnection();
  try {
    await connection.execute(`
      CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE
      )
    `);

    await connection.execute(`
      CREATE TABLE IF NOT EXISTS profiles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        age INT,
        bio VARCHAR(255),
        phone VARCHAR(20),
        address VARCHAR(255)
      )
    `);

    await connection.execute(`
      CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        total_amount DECIMAL(10, 2)
      )
    `);

    await connection.execute(`
      CREATE TABLE IF NOT EXISTS order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        product_name VARCHAR(100),
        price DECIMAL(10, 2)
      )
    `);
  } finally {
    connection.release();
  }
}

app.get('/', async (request, reply) => {
  return { status: 'success', message: 'Node.js Fastify POST Benchmark' };
});

app.post('/raw/post/1table', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    const randomId = crypto.randomBytes(4).toString('hex');
    const email = `node_test_${randomId}_${process.pid}@example.com`;
    const [result] = await connection.execute('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);
    reply.status(201);
    return { user_id: result.insertId };
  } catch (err) {
    reply.status(500);
    return { error: err.message };
  } finally {
    connection.release();
  }
});

app.post('/raw/post/2table', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    await connection.beginTransaction();
    const randomId = crypto.randomBytes(4).toString('hex');
    const email = `node_test_${randomId}_${process.pid}@example.com`;
    const [resUser] = await connection.execute('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);
    const userId = resUser.insertId;
    await connection.execute('INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)', [userId, 25, '123 St', `Bio ${userId}`, `555-${randomId}`]);
    await connection.commit();
    reply.status(201);
    return { user_id: userId };
  } catch (err) {
    await connection.rollback();
    reply.status(500);
    return { error: err.message };
  } finally {
    connection.release();
  }
});

app.post('/raw/post/3table', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    await connection.beginTransaction();
    const randomId = crypto.randomBytes(4).toString('hex');
    const email = `node_test_${randomId}_${process.pid}@example.com`;
    const [resUser] = await connection.execute('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);
    const userId = resUser.insertId;
    await connection.execute('INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)', [userId, 25, '123 St', `Bio ${userId}`, `555-${randomId}`]);
    await connection.execute('INSERT INTO orders (user_id, total_amount) VALUES (?, ?)', [userId, 100.00]);
    await connection.commit();
    reply.status(201);
    return { user_id: userId };
  } catch (err) {
    await connection.rollback();
    reply.status(500);
    return { error: err.message };
  } finally {
    connection.release();
  }
});

app.post('/raw/post/4table', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    await connection.beginTransaction();
    const randomId = crypto.randomBytes(4).toString('hex');
    const email = `node_test_${randomId}_${process.pid}@example.com`;
    const [resUser] = await connection.execute('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);
    const userId = resUser.insertId;
    await connection.execute('INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)', [userId, 25, '123 St', `Bio ${userId}`, `555-${randomId}`]);
    const [resOrder] = await connection.execute('INSERT INTO orders (user_id, total_amount) VALUES (?, ?)', [userId, 100.00]);
    const orderId = resOrder.insertId;
    await connection.execute('INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)', [orderId, `Prod1_${randomId}`, 25.00]);
    await connection.execute('INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)', [orderId, `Prod2_${randomId}`, 75.00]);
    await connection.commit();
    reply.status(201);
    return { user_id: userId };
  } catch (err) {
    await connection.rollback();
    reply.status(500);
    return { error: err.message };
  } finally {
    connection.release();
  }
});

const cluster = require('cluster');
const os = require('os');

if (cluster.isMaster) {
  const numCPUs = os.cpus().length;
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
  cluster.on('exit', () => {
    cluster.fork();
  });
} else {
  initDB().then(() => {
    app.listen({ port: 8002, host: '0.0.0.0' });
  }).catch(err => {
    console.error('Failed to initialize database:', err);
    process.exit(1);
  });
}
