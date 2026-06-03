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
            email VARCHAR(100) UNIQUE
        )");

        $db->exec("CREATE TABLE IF NOT EXISTS profiles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            bio VARCHAR(255),
            phone VARCHAR(20)
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

        
    }

    public function start() {
        $http = new Server('0.0.0.0', 8003);

        $http->set([
            'worker_num' => swoole_cpu_num(),
            'log_file' => '/dev/null'
        ]);
        
        $http->on('WorkerStart', function ($server, $workerId) {
            $db_config = [
                'host' => '127.0.0.1',
                'port' => 3306,
                'user' => 'admin',
                'password' => 'secret',
                'database' => 'benchmark_db'
            ];
            $this->db_pool = new \Swoole\Database\PDOPool(
                (new \Swoole\Database\PDOConfig())
                    ->withDriver('mysql')
                    ->withHost($db_config['host'])
                    ->withPort($db_config['port'])
                    ->withUsername($db_config['user'])
                    ->withPassword($db_config['password'])
                    ->withDbname($db_config['database'])
                    ->withCharset('utf8mb4'),
                100 // Pool size ต่อ Worker
            );
        });
        $http->on('Request', function (Request $request, Response $response) {
            $path = $request->server['path_info'];
            $method = $request->server['request_method'];

            if ($path === '/' && $method === 'GET') {
                $response->setHeader('Content-Type', 'application/json');
                $response->end(json_encode(['status' => 'success', 'message' => 'Hello Benchmark']));
            } elseif ($path === '/raw/post/1table' && $method === 'POST') {
                $this->postRaw1Table($response);
            } elseif ($path === '/raw/post/2table' && $method === 'POST') {
                $this->postRaw2Table($response);
            } elseif ($path === '/raw/post/3table' && $method === 'POST') {
                $this->postRaw3Table($response);
            } elseif ($path === '/raw/post/4table' && $method === 'POST') {
                $this->postRaw4Table($response);
            } else {
                $response->setStatusCode(404);
                $response->end(json_encode(['error' => 'Not found']));
            }
        });

        $http->start();
    }

    private function postRaw1Table(Response $response) {
        $pdo = $this->db_pool->get();
        try {
            $randomId = substr(uniqid(), 0, 8);
            $email = "test_$randomId@example.com";

            $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
            $stmt->execute(["User_$randomId", $email]);

            $userId = $pdo->lastInsertId();

            $response->setStatusCode(201);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode(['user_id' => (int)$userId]));
        } catch (\Exception $e) {
            $response->setStatusCode(500);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode(['error' => $e->getMessage()]));
        } finally {
            $this->db_pool->put($pdo);
        }
    }

    private function postRaw2Table(Response $response) {
        $pdo = $this->db_pool->get();
        try {
            $pdo->beginTransaction();

            $randomId = substr(uniqid(), 0, 8);
            $email = "test_$randomId@example.com";

            $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
            $stmt->execute(["User_$randomId", $email]);
            $userId = $pdo->lastInsertId();

            $stmt = $pdo->prepare("INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)");
            $stmt->execute([$userId, "Bio for user $userId", "555-$randomId"]);

            $pdo->commit();

            $response->setStatusCode(201);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode(['user_id' => (int)$userId]));
        } catch (\Exception $e) {
            $pdo->rollBack();
            $response->setStatusCode(500);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode(['error' => $e->getMessage()]));
        } finally {
            $this->db_pool->put($pdo);
        }
    }

    private function postRaw3Table(Response $response) {
        $pdo = $this->db_pool->get();
        try {
            $pdo->beginTransaction();

            $randomId = substr(uniqid(), 0, 8);
            $email = "test_$randomId@example.com";

            $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
            $stmt->execute(["User_$randomId", $email]);
            $userId = $pdo->lastInsertId();

            $stmt = $pdo->prepare("INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)");
            $stmt->execute([$userId, "Bio for user $userId", "555-$randomId"]);

            $stmt = $pdo->prepare("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)");
            $stmt->execute([$userId, 100.00]);

            $pdo->commit();

            $response->setStatusCode(201);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode(['user_id' => (int)$userId]));
        } catch (\Exception $e) {
            $pdo->rollBack();
            $response->setStatusCode(500);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode(['error' => $e->getMessage()]));
        } finally {
            $this->db_pool->put($pdo);
        }
    }

    private function postRaw4Table(Response $response) {
        $pdo = $this->db_pool->get();
        try {
            $pdo->beginTransaction();

            $randomId = substr(uniqid(), 0, 8);
            $email = "test_$randomId@example.com";

            $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
            $stmt->execute(["User_$randomId", $email]);
            $userId = $pdo->lastInsertId();

            $stmt = $pdo->prepare("INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)");
            $stmt->execute([$userId, "Bio for user $userId", "555-$randomId"]);

            $stmt = $pdo->prepare("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)");
            $stmt->execute([$userId, 100.00]);

            $orderId = $pdo->lastInsertId();

            $stmt = $pdo->prepare("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)");
            $stmt->execute([$orderId, "Product_${randomId}_1", 25.00]);
            $stmt->execute([$orderId, "Product_${randomId}_2", 75.00]);

            $pdo->commit();

            $response->setStatusCode(201);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode(['user_id' => (int)$userId]));
        } catch (\Exception $e) {
            $pdo->rollBack();
            $response->setStatusCode(500);
            $response->setHeader('Content-Type', 'application/json');
            $response->end(json_encode(['error' => $e->getMessage()]));
        } finally {
            $this->db_pool->put($pdo);
        }
    }
}

$server = new BenchmarkServer();
$server->start();
?>
