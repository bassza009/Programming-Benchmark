const fastify = require('fastify');
const mysql = require('mysql2/promise');

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
        email VARCHAR(100),
        INDEX idx_users_email (email)
      )
    `);

    await connection.execute(`
      CREATE TABLE IF NOT EXISTS profiles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        age INT,
        bio VARCHAR(255),
        phone VARCHAR(20),
        address VARCHAR(255),
        INDEX idx_profiles_user_id (user_id)
      )
    `);

    await connection.execute(`
      CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        total_amount DECIMAL(10, 2),
        INDEX idx_orders_user_id (user_id)
      )
    `);

    await connection.execute(`
      CREATE TABLE IF NOT EXISTS order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        product_name VARCHAR(100),
        price DECIMAL(10, 2),
        INDEX idx_order_items_order_id (order_id)
      )
    `);

    const [rows] = await connection.execute('SELECT COUNT(*) as count FROM users');
    if (rows[0].count === 0) {
      await insertMockData(connection);
    }
  } finally {
    connection.release();
  }
}

async function insertMockData(connection) {
  for (let i = 1; i <= 10000; i++) {
    await connection.execute('INSERT INTO users (name, email) VALUES (?, ?)', [`User${i}`, `user${i}@example.com`]);
    await connection.execute('INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)', [i, 20 + (i % 50), `Address ${i}`, `Bio ${i}`, `555-${i}`]);
    await connection.execute('INSERT INTO orders (user_id, total_amount) VALUES (?, ?)', [i, 100.0 + i]);

    if (i % 10 === 0) {
      for (let j = 0; j < 5; j++) {
        await connection.execute('INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)', [i, `Product${j}`, 10.0 + j]);
      }
    }
  }
}

app.get('/', async (request, reply) => {
  return { status: 'success', message: 'Node.js Fastify GET With-Index Benchmark' };
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
