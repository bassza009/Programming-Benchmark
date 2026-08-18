const fastify = require('fastify');
const mysql = require('mysql2/promise');
const cluster = require('cluster');
const os = require('os');
const crypto = require('crypto');

const DB_HOST = process.env.DB_HOST || '127.0.0.1';
const DB_PORT = parseInt(process.env.DB_PORT || '3306');
const DB_USER = process.env.DB_USER || 'admin';
const DB_PASS = process.env.DB_PASS || 'secret';
const DB_NAME = process.env.DB_NAME || 'benchmark_db';

const PORT = 8002;
const numCPUs = Math.min(os.cpus().length, 8);

if (cluster.isPrimary && process.env.NODE_ENV !== 'test') {
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
  cluster.on('exit', (worker) => {
    cluster.fork();
  });
} else {
  const app = fastify({ logger: false });
  let pool;

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

  // ==================== Health Check ====================
  app.get('/', async () => {
    return { status: 'success', language: 'Node.js', framework: 'Fastify', port: PORT };
  });

  // ==================== GET (Read) Endpoints ====================
  app.get('/raw/1table', async (req, reply) => {
    const [rows] = await pool.query('SELECT * FROM users LIMIT 100');
    return reply.send(rows);
  });

  app.get('/raw/2join', async (req, reply) => {
    const [rows] = await pool.query(
      'SELECT u.name, p.age FROM users u JOIN profiles p ON u.id = p.user_id LIMIT 100'
    );
    return reply.send(rows);
  });

  app.get('/raw/3join', async (req, reply) => {
    const [rows] = await pool.query(
      'SELECT u.name, p.age, o.total_amount FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id LIMIT 100'
    );
    return reply.send(rows);
  });

  app.get('/raw/4join', async (req, reply) => {
    const [rows] = await pool.query(
      'SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id JOIN order_items oi ON o.id = oi.order_id LIMIT 100'
    );
    return reply.send(rows);
  });

  // ==================== POST (Write / Transaction) Endpoints ====================
  app.post('/raw/post/1table', async (req, reply) => {
    const randomId = crypto.randomBytes(4).toString('hex');
    const email = `node_${randomId}_${process.pid}@example.com`;
    const [res] = await pool.query('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);
    return reply.status(201).send({ user_id: res.insertId });
  });

  app.post('/raw/post/2table', async (req, reply) => {
    const conn = await pool.getConnection();
    try {
      await conn.beginTransaction();
      const randomId = crypto.randomBytes(4).toString('hex');
      const email = `node_${randomId}_${process.pid}@example.com`;
      const [uRes] = await conn.query('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);
      const userId = uRes.insertId;
      await conn.query(
        'INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)',
        [userId, 25, '123 Main St', `Bio ${userId}`, `555-${randomId}`]
      );
      await conn.commit();
      return reply.status(201).send({ user_id: userId });
    } catch (err) {
      await conn.rollback();
      return reply.status(500).send({ error: err.message });
    } finally {
      conn.release();
    }
  });

  app.post('/raw/post/3table', async (req, reply) => {
    const conn = await pool.getConnection();
    try {
      await conn.beginTransaction();
      const randomId = crypto.randomBytes(4).toString('hex');
      const email = `node_${randomId}_${process.pid}@example.com`;
      const [uRes] = await conn.query('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);
      const userId = uRes.insertId;
      await conn.query(
        'INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)',
        [userId, 25, '123 Main St', `Bio ${userId}`, `555-${randomId}`]
      );
      await conn.query('INSERT INTO orders (user_id, total_amount) VALUES (?, ?)', [userId, 100.00]);
      await conn.commit();
      return reply.status(201).send({ user_id: userId });
    } catch (err) {
      await conn.rollback();
      return reply.status(500).send({ error: err.message });
    } finally {
      conn.release();
    }
  });

  app.post('/raw/post/4table', async (req, reply) => {
    const conn = await pool.getConnection();
    try {
      await conn.beginTransaction();
      const randomId = crypto.randomBytes(4).toString('hex');
      const email = `node_${randomId}_${process.pid}@example.com`;
      const [uRes] = await conn.query('INSERT INTO users (name, email) VALUES (?, ?)', [`User_${randomId}`, email]);
      const userId = uRes.insertId;
      await conn.query(
        'INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)',
        [userId, 25, '123 Main St', `Bio ${userId}`, `555-${randomId}`]
      );
      const [oRes] = await conn.query('INSERT INTO orders (user_id, total_amount) VALUES (?, ?)', [userId, 100.00]);
      const orderId = oRes.insertId;
      await conn.query(
        'INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)',
        [orderId, `Item1_${randomId}`, 25.00]
      );
      await conn.query(
        'INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)',
        [orderId, `Item2_${randomId}`, 75.00]
      );
      await conn.commit();
      return reply.status(201).send({ user_id: userId });
    } catch (err) {
      await conn.rollback();
      return reply.status(500).send({ error: err.message });
    } finally {
      conn.release();
    }
  });

  app.listen({ port: PORT, host: '0.0.0.0' }, (err) => {
    if (err) {
      process.exit(1);
    }
  });
}
