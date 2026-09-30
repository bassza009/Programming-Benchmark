const fastify = require('fastify');
const { Pool } = require('pg');
const cluster = require('cluster');
const os = require('os');
const crypto = require('crypto');

const DB_HOST = process.env.DB_HOST || '127.0.0.1';
const DB_PORT = parseInt(process.env.DB_PORT || '5432', 10);
const DB_USER = process.env.DB_USER || 'admin';
const DB_PASS = process.env.DB_PASS || 'secret';
const DB_NAME = process.env.DB_NAME || 'benchmark_db';

let pool;

function getPool() {
  if (!pool) {
    pool = new Pool({
      host: DB_HOST,
      port: DB_PORT,
      user: DB_USER,
      password: DB_PASS,
      database: DB_NAME,
      max: 50,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 5000,
    });
  }
  return pool;
}

function startWorker() {
  const app = fastify({ logger: false });
  const p = getPool();

  app.get('/', async (req, reply) => {
    return { status: 'success', message: 'Node.js Fastify PostgreSQL POST Benchmark' };
  });

  app.post('/raw/post/1table', async (req, reply) => {
    const uid = crypto.randomUUID().substring(0, 8);
    const email = `node_${uid}_${Date.now()}@example.com`;
    const res = await p.query(
      'INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id',
      [`Customer_${uid}`, email, `555-${uid}`, 'Benchmark City']
    );
    reply.status(201);
    return { customer_id: res.rows[0].id };
  });

  app.post('/raw/post/2table', async (req, reply) => {
    const client = await p.connect();
    try {
      await client.query('BEGIN');
      const uid = crypto.randomUUID().substring(0, 8);
      const email = `node_${uid}_${Date.now()}@example.com`;
      const resCust = await client.query(
        'INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id',
        [`Customer_${uid}`, email, `555-${uid}`, 'Benchmark City']
      );
      const customerId = resCust.rows[0].id;
      const resOrder = await client.query(
        'INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES ($1, $2, $3, $4, $5) RETURNING id',
        [customerId, 1, 2, 150.00, 'COMPLETED']
      );
      await client.query('COMMIT');
      reply.status(201);
      return { customer_id: customerId, order_id: resOrder.rows[0].id };
    } catch (err) {
      await client.query('ROLLBACK');
      reply.status(500);
      return { error: err.message };
    } finally {
      client.release();
    }
  });

  app.post('/raw/post/3table', async (req, reply) => {
    const client = await p.connect();
    try {
      await client.query('BEGIN');
      const uid = crypto.randomUUID().substring(0, 8);
      const email = `node_${uid}_${Date.now()}@example.com`;
      const resCust = await client.query(
        'INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id',
        [`Customer_${uid}`, email, `555-${uid}`, 'Benchmark City']
      );
      const customerId = resCust.rows[0].id;
      const resProd = await client.query(
        'INSERT INTO product (factory_id, name, category, price, stock) VALUES ($1, $2, $3, $4, $5) RETURNING id',
        [1, `Product_${uid}`, 'Benchmark Category', 99.99, 100]
      );
      const productId = resProd.rows[0].id;
      const resOrder = await client.query(
        'INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES ($1, $2, $3, $4, $5) RETURNING id',
        [customerId, productId, 1, 99.99, 'COMPLETED']
      );
      await client.query('COMMIT');
      reply.status(201);
      return { customer_id: customerId, product_id: productId, order_id: resOrder.rows[0].id };
    } catch (err) {
      await client.query('ROLLBACK');
      reply.status(500);
      return { error: err.message };
    } finally {
      client.release();
    }
  });

  app.post('/raw/post/4table', async (req, reply) => {
    const client = await p.connect();
    try {
      await client.query('BEGIN');
      const uid = crypto.randomUUID().substring(0, 8);
      const email = `node_${uid}_${Date.now()}@example.com`;
      const resFact = await client.query(
        'INSERT INTO factory (name, location, country) VALUES ($1, $2, $3) RETURNING id',
        [`Factory_${uid}`, 'Industrial Estate', 'Thailand']
      );
      const factoryId = resFact.rows[0].id;
      const resProd = await client.query(
        'INSERT INTO product (factory_id, name, category, price, stock) VALUES ($1, $2, $3, $4, $5) RETURNING id',
        [factoryId, `Product_${uid}`, 'Benchmark Category', 99.99, 100]
      );
      const productId = resProd.rows[0].id;
      const resCust = await client.query(
        'INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id',
        [`Customer_${uid}`, email, `555-${uid}`, 'Benchmark City']
      );
      const customerId = resCust.rows[0].id;
      const resOrder = await client.query(
        'INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES ($1, $2, $3, $4, $5) RETURNING id',
        [customerId, productId, 1, 99.99, 'COMPLETED']
      );
      await client.query('COMMIT');
      reply.status(201);
      return { factory_id: factoryId, product_id: productId, customer_id: customerId, order_id: resOrder.rows[0].id };
    } catch (err) {
      await client.query('ROLLBACK');
      reply.status(500);
      return { error: err.message };
    } finally {
      client.release();
    }
  });

  app.listen({ port: 8002, host: '0.0.0.0' }, (err) => {
    if (err) process.exit(1);
  });
}

if (cluster.isPrimary || cluster.isMaster) {
  const numCPUs = os.cpus().length;
  for (let i = 0; i < numCPUs; i++) cluster.fork();
  cluster.on('exit', () => cluster.fork());
} else {
  startWorker();
}
