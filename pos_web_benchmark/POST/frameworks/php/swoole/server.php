<?php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;
use Swoole\Database\PDOConfig;
use Swoole\Database\PDOPool;

class BenchmarkPostServer {
    private $db_config;
    private $pool = null;

    public function __construct() {
        $this->db_config = [
            'host' => getenv('DB_HOST') ?: '127.0.0.1',
            'port' => (int)(getenv('DB_PORT') ?: 5432),
            'user' => getenv('DB_USER') ?: 'admin',
            'password' => getenv('DB_PASS') ?: 'secret',
            'database' => getenv('DB_NAME') ?: 'benchmark_db'
        ];
    }

    public function initPool($size = 64) {
        if (class_exists('Swoole\Database\PDOPool')) {
            $config = (new PDOConfig())
                ->withHost($this->db_config['host'])
                ->withPort($this->db_config['port'])
                ->withDbName($this->db_config['database'])
                ->withUsername($this->db_config['user'])
                ->withPassword($this->db_config['password'])
                ->withDriver('pgsql')
                ->withOptions([
                    \PDO::ATTR_ERRMODE => \PDO::ERRMODE_EXCEPTION,
                    \PDO::ATTR_DEFAULT_FETCH_MODE => \PDO::FETCH_ASSOC
                ]);
            $this->pool = new PDOPool($config, $size);
        }
    }

    public function run() {
        $server = new Server("0.0.0.0", 8003);

        $server->set([
            'worker_num' => swoole_cpu_num() * 2,
            'max_request' => 0,
            'enable_coroutine' => true,
            'log_level' => SWOOLE_LOG_ERROR,
            'open_tcp_nodelay' => true,
            'max_coroutine' => 100000,
        ]);

        $server->on("WorkerStart", function($server, $worker_id) {
            $this->initPool(64);
        });

        $server->on("request", function(Request $request, Response $response) {
            $path = $request->server['request_uri'];
            $method = $request->server['request_method'];
            $response->header("Content-Type", "application/json");

            if ($path === '/' && $method === 'GET') {
                $response->end(json_encode(["status" => "success", "message" => "PHP Swoole PostgreSQL POST Benchmark"]));
                return;
            }

            if ($method !== 'POST') {
                $response->status(405);
                $response->end(json_encode(["error" => "Method not allowed"]));
                return;
            }

            $pdo = $this->pool ? $this->pool->get() : null;
            if (!$pdo) {
                $response->status(500);
                $response->end(json_encode(["error" => "Database connection failure"]));
                return;
            }

            $uid = bin2hex(random_bytes(4));
            $email = "php_{$uid}_" . hrtime(true) . "@example.com";

            try {
                if ($path === '/raw/post/1table') {
                    $stmt = $pdo->prepare("INSERT INTO customer (name, email, phone, city) VALUES (?, ?, ?, ?) RETURNING id");
                    $stmt->execute(["Customer_{$uid}", $email, "555-{$uid}", "Benchmark City"]);
                    $customerId = $stmt->fetchColumn();
                    $response->status(201);
                    $response->end(json_encode(["customer_id" => $customerId]));
                } elseif ($path === '/raw/post/2table') {
                    $pdo->beginTransaction();
                    $stmtCust = $pdo->prepare("INSERT INTO customer (name, email, phone, city) VALUES (?, ?, ?, ?) RETURNING id");
                    $stmtCust->execute(["Customer_{$uid}", $email, "555-{$uid}", "Benchmark City"]);
                    $customerId = $stmtCust->fetchColumn();

                    $stmtOrder = $pdo->prepare("INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES (?, 1, 2, 150.00, 'COMPLETED') RETURNING id");
                    $stmtOrder->execute([$customerId]);
                    $orderId = $stmtOrder->fetchColumn();

                    $pdo->commit();
                    $response->status(201);
                    $response->end(json_encode(["customer_id" => $customerId, "order_id" => $orderId]));
                } elseif ($path === '/raw/post/3table') {
                    $pdo->beginTransaction();
                    $stmtCust = $pdo->prepare("INSERT INTO customer (name, email, phone, city) VALUES (?, ?, ?, ?) RETURNING id");
                    $stmtCust->execute(["Customer_{$uid}", $email, "555-{$uid}", "Benchmark City"]);
                    $customerId = $stmtCust->fetchColumn();

                    $stmtProd = $pdo->prepare("INSERT INTO product (factory_id, name, category, price, stock) VALUES (1, ?, 'Benchmark Category', 99.99, 100) RETURNING id");
                    $stmtProd->execute(["Product_{$uid}"]);
                    $productId = $stmtProd->fetchColumn();

                    $stmtOrder = $pdo->prepare("INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES (?, ?, 1, 99.99, 'COMPLETED') RETURNING id");
                    $stmtOrder->execute([$customerId, $productId]);
                    $orderId = $stmtOrder->fetchColumn();

                    $pdo->commit();
                    $response->status(201);
                    $response->end(json_encode(["customer_id" => $customerId, "product_id" => $productId, "order_id" => $orderId]));
                } elseif ($path === '/raw/post/4table') {
                    $pdo->beginTransaction();
                    $stmtFact = $pdo->prepare("INSERT INTO factory (name, location, country) VALUES (?, 'Industrial Estate', 'Thailand') RETURNING id");
                    $stmtFact->execute(["Factory_{$uid}"]);
                    $factoryId = $stmtFact->fetchColumn();

                    $stmtProd = $pdo->prepare("INSERT INTO product (factory_id, name, category, price, stock) VALUES (?, ?, 'Benchmark Category', 99.99, 100) RETURNING id");
                    $stmtProd->execute([$factoryId, "Product_{$uid}"]);
                    $productId = $stmtProd->fetchColumn();

                    $stmtCust = $pdo->prepare("INSERT INTO customer (name, email, phone, city) VALUES (?, ?, ?, ?) RETURNING id");
                    $stmtCust->execute(["Customer_{$uid}", $email, "555-{$uid}", "Benchmark City"]);
                    $customerId = $stmtCust->fetchColumn();

                    $stmtOrder = $pdo->prepare("INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES (?, ?, 1, 99.99, 'COMPLETED') RETURNING id");
                    $stmtOrder->execute([$customerId, $productId]);
                    $orderId = $stmtOrder->fetchColumn();

                    $pdo->commit();
                    $response->status(201);
                    $response->end(json_encode([
                        "factory_id" => $factoryId,
                        "product_id" => $productId,
                        "customer_id" => $customerId,
                        "order_id" => $orderId
                    ]));
                } else {
                    $response->status(404);
                    $response->end(json_encode(["error" => "Endpoint not found"]));
                }
            } catch (\Throwable $e) {
                if ($pdo->inTransaction()) {
                    $pdo->rollBack();
                }
                $response->status(500);
                $response->end(json_encode(["error" => $e->getMessage()]));
            } finally {
                if ($this->pool && $pdo) {
                    $this->pool->put($pdo);
                }
            }
        });

        $server->start();
    }
}

$app = new BenchmarkPostServer();
$app->run();
