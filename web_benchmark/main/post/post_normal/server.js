const fastify = require('fastify');
const mysql = require('mysql2/promise');
const { v4: uuidv4 } = require('uuid');

const app = fastify({ logger: false });
let pool;

async function initDB() {
  pool = await mysql.createPool({
    host: '127.0.0.1',
    port: 3306,
    user: 'admin',
    password: 'secret',
    database: 'benchmark_db',
    waitForConnections: true,
    connectionLimit: 100,
    queueLimit: 0
  });

  const connection = await pool.getConnection();

  // Create tables
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
      bio VARCHAR(255),
      phone VARCHAR(20)
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

  connection.release();
}

app.get('/', async (request, reply) => {
  return { status: 'success', message: 'Hello Benchmark' };
});

app.post('/raw/post/1table', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    const randomId = uuidv4().substring(0, 8);
    const email = `test_${randomId}@example.com`;

    await connection.execute('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);

    const [result] = await connection.execute('SELECT LAST_INSERT_ID() as id');
    const userId = result[0].id;

    reply.code(201);
    return { user_id: userId };
  } catch (error) {
    reply.code(500);
    return { error: error.message };
  } finally {
    connection.release();
  }
});

app.post('/raw/post/2table', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    await connection.beginTransaction();

    const randomId = uuidv4().substring(0, 8);
    const email = `test_${randomId}@example.com`;

    await connection.execute('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);

    const [result] = await connection.execute('SELECT LAST_INSERT_ID() as id');
    const userId = result[0].id;

    await connection.execute('INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)',
      [userId, `Bio for user ${userId}`, `555-${randomId}`]);

    await connection.commit();
    reply.code(201);
    return { user_id: userId };
  } catch (error) {
    await connection.rollback();
    reply.code(500);
    return { error: error.message };
  } finally {
    connection.release();
  }
});

app.post('/raw/post/3table', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    await connection.beginTransaction();

    const randomId = uuidv4().substring(0, 8);
    const email = `test_${randomId}@example.com`;

    await connection.execute('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);

    const [result] = await connection.execute('SELECT LAST_INSERT_ID() as id');
    const userId = result[0].id;

    await connection.execute('INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)',
      [userId, `Bio for user ${userId}`, `555-${randomId}`]);

    await connection.execute('INSERT INTO orders (user_id, total_amount) VALUES (?, ?)',
      [userId, 100.00]);

    await connection.commit();
    reply.code(201);
    return { user_id: userId };
  } catch (error) {
    await connection.rollback();
    reply.code(500);
    return { error: error.message };
  } finally {
    connection.release();
  }
});

app.post('/raw/post/4table', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    await connection.beginTransaction();

    const randomId = uuidv4().substring(0, 8);
    const email = `test_${randomId}@example.com`;

    await connection.execute('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);

    const [result] = await connection.execute('SELECT LAST_INSERT_ID() as id');
    const userId = result[0].id;

    await connection.execute('INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)',
      [userId, `Bio for user ${userId}`, `555-${randomId}`]);

    await connection.execute('INSERT INTO orders (user_id, total_amount) VALUES (?, ?)',
      [userId, 100.00]);

    const [orderResult] = await connection.execute('SELECT LAST_INSERT_ID() as id');
    const orderId = orderResult[0].id;

    await connection.execute('INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)',
      [orderId, `Product_${randomId}_1`, 25.00]);
    await connection.execute('INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)',
      [orderId, `Product_${randomId}_2`, 75.00]);

    await connection.commit();
    reply.code(201);
    return { user_id: userId };
  } catch (error) {
    await connection.rollback();
    reply.code(500);
    return { error: error.message };
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
  cluster.on('exit', (worker) => {
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
