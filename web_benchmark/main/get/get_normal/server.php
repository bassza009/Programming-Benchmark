<?php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;

class BenchmarkServer {
    private $db_pool;

    public function __construct() {
        $this->initDatabase();
    }

    private function initDatabase() {
        $db_config = [
            'host' => '127.0.0.1',
            'port' => 3306,
            'user' => 'admin',
            'password' => 'secret',
            'database' => 'benchmark_db'
        ];

        // Create initial connection to set up schema
        $db = new \PDO(
            'mysql:host=' . $db_config['host'] . ';port=' . $db_config['port'],
            $db_config['user'],
            $db_config['password']
        );

        $db->exec("CREATE DATABASE IF NOT EXISTS benchmark_db");
        $db->exec("USE benchmark_db");

        // Create tables
        $db->exec("CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        )");

        $db->exec("CREATE TABLE IF NOT EXISTS profiles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            age INT,
            address VARCHAR(255)
        )");

        $db->exec("CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            total_amount DECIMAL(10, 2)
        )");

        $db->exec("CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            product_name VARCHAR(100),
            price DECIMAL(10, 2)
        )");

        // Check if data exists
        $stmt = $db->query("SELECT COUNT(*) FROM users");
        $count = $stmt->fetchColumn();

        if ($count == 0) {
            $this->insertMockData($db);
        }

        // Create Swoole connection pool
        $this->db_pool = new \Swoole\Database\PDOPool(
            (new \Swoole\Database\PDOConfig())
                ->withDriver('mysql')
                ->withHost($db_config['host'])
                ->withPort($db_config['port'])
                ->withUsername($db_config['user'])
                ->withPassword($db_config['password'])
                ->withDbname($db_config['database'])
                ->withCharset('utf8mb4'),
            100
        );
    }

    private function insertMockData($db) {
        $db->beginTransaction();
        try {
            for ($i = 1; $i <= 10000; $i++) {
                $db->exec("INSERT INTO users (name, email) VALUES ('User$i', 'user$i@example.com')");
                $db->exec("INSERT INTO profiles (user_id, age, address) VALUES ($i, " . (20 + ($i % 50)) . ", 'Address $i')");
                $db->exec("INSERT INTO orders (user_id, total_amount) VALUES ($i, " . (100.0 + $i) . ")");

                if ($i % 10 == 0) {
                    for ($j = 0; $j < 5; $j++) {
                        $db->exec("INSERT INTO order_items (order_id, product_name, price) VALUES ($i, 'Product$j', " . (10.0 + $j) . ")");
                    }
                }
            }
            $db->commit();
        } catch (\Exception $e) {
            $db->rollBack();
            throw $e;
        }
    }

    public function start() {
        $http = new Server('0.0.0.0', 8003);

        $http->set([
            'worker_num' => swoole_cpu_num(),
            'log_file' => '/dev/null'
        ]);

        $http->on('Request', function (Request $request, Response $response) {
            $path = $request->server['path_info'];

            if ($path === '/') {
                $response->setHeader('Content-Type', 'application/json');
                $response->end(json_encode(['status' => 'success', 'message' => 'Hello Benchmark']));
            } elseif ($path === '/raw/1table') {
                $this->raw1Table($response);
            } elseif ($path === '/raw/2join') {
                $this->raw2Join($response);
            } elseif ($path === '/raw/3join') {
                $this->raw3Join($response);
            } elseif ($path === '/raw/4join') {
                $this->raw4Join($response);
            } else {
                $response->setStatusCode(404);
                $response->end(json_encode(['error' => 'Not found']));
            }
        });

        $http->start();
    }

    private function raw1Table(Response $response) {
        $pdo = $this->db_pool->get();
        try {
            $stmt = $pdo->query("SELECT * FROM users LIMIT 100");
            $results = $stmt->fetchAll(\PDO::FETCH_ASSOC);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode($results));
        } finally {
            $this->db_pool->put($pdo);
        }
    }

    private function raw2Join(Response $response) {
        $pdo = $this->db_pool->get();
        try {
            $stmt = $pdo->query("SELECT u.name, p.age FROM users u JOIN profiles p ON u.id = p.user_id LIMIT 100");
            $results = $stmt->fetchAll(\PDO::FETCH_ASSOC);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode($results));
        } finally {
            $this->db_pool->put($pdo);
        }
    }

    private function raw3Join(Response $response) {
        $pdo = $this->db_pool->get();
        try {
            $stmt = $pdo->query("SELECT u.name, p.age, o.total_amount FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id LIMIT 100");
            $results = $stmt->fetchAll(\PDO::FETCH_ASSOC);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode($results));
        } finally {
            $this->db_pool->put($pdo);
        }
    }

    private function raw4Join(Response $response) {
        $pdo = $this->db_pool->get();
        try {
            $stmt = $pdo->query("SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id JOIN order_items oi ON o.id = oi.order_id LIMIT 100");
            $results = $stmt->fetchAll(\PDO::FETCH_ASSOC);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode($results));
        } finally {
            $this->db_pool->put($pdo);
        }
    }
}

$server = new BenchmarkServer();
$server->start();
?>
