const fastify = require('fastify');
const { Pool } = require('pg');
const cluster = require('cluster');
const os = require('os');

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
    return { status: 'success', message: 'Node.js Fastify PostgreSQL GET Benchmark' };
  });

  app.get('/raw/1table', async (req, reply) => {
    const res = await p.query('SELECT id, name, email, phone, city, created_at FROM customer LIMIT 100');
    return res.rows;
  });

  app.get('/raw/2join', async (req, reply) => {
    const res = await p.query(`
      SELECT o.id, c.name, o.quantity, o.total_amount, o.order_date
      FROM orders o
      JOIN customer c ON o.customer_id = c.id
      LIMIT 100
    `);
    return res.rows;
  });

  app.get('/raw/3join', async (req, reply) => {
    const res = await p.query(`
      SELECT o.id, c.name, p.name AS product_name, o.quantity, o.total_amount
      FROM orders o
      JOIN customer c ON o.customer_id = c.id
      JOIN product p ON o.product_id = p.id
      LIMIT 100
    `);
    return res.rows;
  });

  app.get('/raw/4join', async (req, reply) => {
    const res = await p.query(`
      SELECT o.id, c.name, p.name AS product_name, f.name AS factory_name, o.quantity, o.total_amount
      FROM orders o
      JOIN customer c ON o.customer_id = c.id
      JOIN product p ON o.product_id = p.id
      JOIN factory f ON p.factory_id = f.id
      LIMIT 100
    `);
    return res.rows;
  });

  app.listen({ port: 8002, host: '0.0.0.0' }, (err) => {
    if (err) {
      process.exit(1);
    }
  });
}

if (cluster.isPrimary || cluster.isMaster) {
  const numCPUs = os.cpus().length;
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
  cluster.on('exit', () => {
    cluster.fork();
  });
} else {
  startWorker();
}
