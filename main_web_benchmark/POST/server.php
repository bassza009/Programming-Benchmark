<?php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;

class AntigravityPostServer {
    private $db_config;

    public function __construct() {
        $this->db_config = [
            'host' => getenv('DB_HOST') ?: '127.0.0.1',
            'port' => getenv('DB_PORT') ?: 3306,
            'user' => getenv('DB_USER') ?: 'admin',
            'password' => getenv('DB_PASS') ?: 'secret',
            'database' => getenv('DB_NAME') ?: 'benchmark_db'
        ];
        $this->initDatabase();
    }

    private function initDatabase() {
        try {
            $db = new \PDO(
                'mysql:host=' . $this->db_config['host'] . ';port=' . $this->db_config['port'],
                $this->db_config['user'],
                $this->db_config['password'],
                [\PDO::ATTR_ERRMODE => \PDO::ERRMODE_EXCEPTION]
            );

            $db->exec("CREATE DATABASE IF NOT EXISTS " . $this->db_config['database']);
            $db->exec("USE " . $this->db_config['database']);

            $db->exec("CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE
            )");

            $db->exec("CREATE TABLE IF NOT EXISTS profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                age INT,
                bio VARCHAR(255),
                phone VARCHAR(20),
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
        } catch (\Exception $e) {
            error_log("Database Init Error: " . $e->getMessage());
        }
    }

    private function getPDO() {
        return new \PDO(
            'mysql:host=' . $this->db_config['host'] . ';port=' . $this->db_config['port'] . ';dbname=' . $this->db_config['database'],
            $this->db_config['user'],
            $this->db_config['password'],
            [
                \PDO::ATTR_ERRMODE => \PDO::ERRMODE_EXCEPTION,
                \PDO::ATTR_DEFAULT_FETCH_MODE => \PDO::FETCH_ASSOC
            ]
        );
    }

    public function handleRequest(Request $request, Response $response) {
        $uri = $request->server['request_uri'];
        $response->header("Content-Type", "application/json");

        try {
            $pdo = $this->getPDO();

            if ($uri === '/') {
                $response->status(200);
                $response->end(json_encode(["status" => "success", "message" => "PHP Swoole POST Benchmark"]));
                return;
            }

            $randId = substr(md5(uniqid(mt_rand(), true)), 0, 8);
            $email = "php_test_{$randId}_" . getmypid() . "@example.com";

            if ($uri === '/raw/post/1table') {
                $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
                $stmt->execute(["User_$randId", $email]);
                $userId = $pdo->lastInsertId();
                $response->status(201);
                $response->end(json_encode(["user_id" => (int)$userId]));
                return;
            }

            if ($uri === '/raw/post/2table') {
                $pdo->beginTransaction();
                $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
                $stmt->execute(["User_$randId", $email]);
                $userId = $pdo->lastInsertId();

                $stmt = $pdo->prepare("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)");
                $stmt->execute([$userId, 25, "123 St", "Bio $userId", "555-$randId"]);
                $pdo->commit();

                $response->status(201);
                $response->end(json_encode(["user_id" => (int)$userId]));
                return;
            }

            if ($uri === '/raw/post/3table') {
                $pdo->beginTransaction();
                $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
                $stmt->execute(["User_$randId", $email]);
                $userId = $pdo->lastInsertId();

                $stmt = $pdo->prepare("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)");
                $stmt->execute([$userId, 25, "123 St", "Bio $userId", "555-$randId"]);

                $stmt = $pdo->prepare("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)");
                $stmt->execute([$userId, 100.00]);
                $pdo->commit();

                $response->status(201);
                $response->end(json_encode(["user_id" => (int)$userId]));
                return;
            }

            if ($uri === '/raw/post/4table') {
                $pdo->beginTransaction();
                $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
                $stmt->execute(["User_$randId", $email]);
                $userId = $pdo->lastInsertId();

                $stmt = $pdo->prepare("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)");
                $stmt->execute([$userId, 25, "123 St", "Bio $userId", "555-$randId"]);

                $stmt = $pdo->prepare("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)");
                $stmt->execute([$userId, 100.00]);
                $orderId = $pdo->lastInsertId();

                $stmt = $pdo->prepare("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)");
                $stmt->execute([$orderId, "Prod1_$randId", 25.00]);
                $stmt->execute([$orderId, "Prod2_$randId", 75.00]);
                $pdo->commit();

                $response->status(201);
                $response->end(json_encode(["user_id" => (int)$userId]));
                return;
            }

            $response->status(404);
            $response->end(json_encode(["error" => "Not Found"]));
        } catch (\Exception $e) {
            $response->status(500);
            $response->end(json_encode(["error" => $e->getMessage()]));
        }
    }
}

$server = new Server("0.0.0.0", 8003);
$antigravity = new AntigravityPostServer();

$server->set([
    'worker_num' => swoole_cpu_num() * 2,
    'enable_coroutine' => true,
    'log_level' => SWOOLE_LOG_ERROR
]);

$server->on("request", function (Request $request, Response $response) use ($antigravity) {
    $antigravity->handleRequest($request, $response);
});

$server->start();
