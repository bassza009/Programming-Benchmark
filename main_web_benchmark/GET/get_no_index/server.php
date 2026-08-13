<?php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;

class AntigravityGetNoIndexServer {
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
                email VARCHAR(100)
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

            $stmt = $db->query("SELECT COUNT(*) FROM users");
            if ($stmt->fetchColumn() == 0) {
                $this->insertMockData($db);
            }
        } catch (\Exception $e) {
            error_log("Database Init Error: " . $e->getMessage());
        }
    }

    private function insertMockData($db) {
        $db->beginTransaction();
        for ($i = 1; $i <= 10000; $i++) {
            $stmt = $db->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
            $stmt->execute(["User$i", "user{$i}@example.com"]);

            $stmt = $db->prepare("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)");
            $stmt->execute([$i, 20 + ($i % 50), "Address $i", "Bio $i", "555-$i"]);

            $stmt = $db->prepare("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)");
            $stmt->execute([$i, 100.0 + $i]);

            if ($i % 10 == 0) {
                for ($j = 0; $j < 5; $j++) {
                    $stmt = $db->prepare("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)");
                    $stmt->execute([$i, "Product$j", 10.0 + $j]);
                }
            }
        }
        $db->commit();
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
                $response->end(json_encode(["status" => "success", "message" => "PHP Swoole GET No-Index Benchmark"]));
                return;
            }
            if ($uri === '/raw/1table') {
                $stmt = $pdo->query("SELECT * FROM users LIMIT 100");
                $response->status(200);
                $response->end(json_encode($stmt->fetchAll()));
                return;
            }
            if ($uri === '/raw/2join') {
                $stmt = $pdo->query("SELECT u.name, p.age FROM users u JOIN profiles p ON u.id = p.user_id LIMIT 100");
                $response->status(200);
                $response->end(json_encode($stmt->fetchAll()));
                return;
            }
            if ($uri === '/raw/3join') {
                $stmt = $pdo->query("SELECT u.name, p.age, o.total_amount FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id LIMIT 100");
                $response->status(200);
                $response->end(json_encode($stmt->fetchAll()));
                return;
            }
            if ($uri === '/raw/4join') {
                $stmt = $pdo->query("SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id JOIN order_items oi ON o.id = oi.order_id LIMIT 100");
                $response->status(200);
                $response->end(json_encode($stmt->fetchAll()));
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
$antigravity = new AntigravityGetNoIndexServer();

$server->set([
    'worker_num' => swoole_cpu_num() * 2,
    'enable_coroutine' => true,
    'log_level' => SWOOLE_LOG_ERROR
]);

$server->on("request", function (Request $request, Response $response) use ($antigravity) {
    $antigravity->handleRequest($request, $response);
});

$server->start();
