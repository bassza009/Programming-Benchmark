const fastify = require('fastify');
const mysql = require('mysql2/promise');
const cluster = require('cluster');
const os = require('os');

const app = fastify({ logger: false });
let pool;

const DB_HOST = process.env.DB_HOST || '127.0.0.1';
const DB_PORT = parseInt(process.env.DB_PORT || '3306');
const DB_USER = process.env.DB_USER || 'admin';
const DB_PASS = process.env.DB_PASS || 'secret';
const DB_NAME = process.env.DB_NAME || 'benchmark_db';

async function initDB() {
  const conn = await mysql.createConnection({
    host: DB_HOST,
    port: DB_PORT,
    user: DB_USER,
    password: DB_PASS,
    database: DB_NAME
  });

  try {
    await conn.execute(`
      CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
      )
    `);

    await conn.execute(`
      CREATE TABLE IF NOT EXISTS profiles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        age INT,
        bio VARCHAR(255),
        phone VARCHAR(20),
        address VARCHAR(255)
      )
    `);

    await conn.execute(`
      CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        total_amount DECIMAL(10, 2)
      )
    `);

    await conn.execute(`
      CREATE TABLE IF NOT EXISTS order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        product_name VARCHAR(100),
        price DECIMAL(10, 2)
      )
    `);

    const [rows] = await conn.execute('SELECT COUNT(*) as count FROM users');
    if (rows[0].count === 0) {
      await insertMockData(conn);
    }
  } finally {
    await conn.end();
  }
}

async function insertMockData(conn) {
  const BATCH_SIZE = 1000;
  for (let start = 1; start <= 10000; start += BATCH_SIZE) {
    const end = start + BATCH_SIZE - 1;
    const users = [];
    const profiles = [];
    const orders = [];
    const items = [];
    for (let i = start; i <= end; i++) {
      users.push([`User${i}`, `user${i}@example.com`]);
      profiles.push([i, 20 + (i % 50), `Address ${i}`, `Bio ${i}`, `555-${i}`]);
      orders.push([i, 100.0 + i]);
      if (i % 10 === 0) {
        for (let j = 0; j < 5; j++) {
          items.push([i, `Product${j}`, 10.0 + j]);
        }
      }
    }
    await conn.query('INSERT INTO users (name, email) VALUES ?', [users]);
    await conn.query('INSERT INTO profiles (user_id, age, address, bio, phone) VALUES ?', [profiles]);
    await conn.query('INSERT INTO orders (user_id, total_amount) VALUES ?', [orders]);
    if (items.length > 0) {
      await conn.query('INSERT INTO order_items (order_id, product_name, price) VALUES ?', [items]);
    }
  }
}

app.get('/', async (request, reply) => {
  return { status: 'success', message: 'Node.js Fastify GET No-Index Benchmark' };
});

app.get('/raw/1table', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    const [rows] = await connection.execute('SELECT * FROM users LIMIT 100');
    return rows;
  } finally {
    connection.release();
  }
});

app.get('/raw/2join', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    const [rows] = await connection.execute('SELECT u.name, p.age FROM users u JOIN profiles p ON u.id = p.user_id LIMIT 100');
    return rows;
  } finally {
    connection.release();
  }
});

app.get('/raw/3join', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    const [rows] = await connection.execute('SELECT u.name, p.age, o.total_amount FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id LIMIT 100');
    return rows;
  } finally {
    connection.release();
  }
});

app.get('/raw/4join', async (request, reply) => {
  const connection = await pool.getConnection();
  try {
    const [rows] = await connection.execute('SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id JOIN order_items oi ON o.id = oi.order_id LIMIT 100');
    return rows;
  } finally {
    connection.release();
  }
});

if (cluster.isPrimary || cluster.isMaster) {
  initDB().then(() => {
    const numCPUs = Math.min(os.cpus().length, 8);
    for (let i = 0; i < numCPUs; i++) {
      cluster.fork();
    }
    cluster.on('exit', () => {
      cluster.fork();
    });
  }).catch(err => {
    console.error('Failed to initialize database:', err);
    process.exit(1);
  });
} else {
  pool = mysql.createPool({
    host: DB_HOST,
    port: DB_PORT,
    user: DB_USER,
    password: DB_PASS,
    database: DB_NAME,
    waitForConnections: true,
    connectionLimit: 50,
    queueLimit: 0
  });

  app.listen({ port: 8002, host: '0.0.0.0' }, (err) => {
    if (err) {
      console.error('Failed to start server:', err);
      process.exit(1);
    }
  });
}
