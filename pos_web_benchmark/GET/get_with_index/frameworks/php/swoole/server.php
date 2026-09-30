<?php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;
use Swoole\Database\PDOConfig;
use Swoole\Database\PDOPool;

class BenchmarkGetServer {
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
            $response->header("Content-Type", "application/json");

            if ($path === '/') {
                $response->end(json_encode(["status" => "success", "message" => "PHP Swoole PostgreSQL GET Benchmark"]));
                return;
            }

            $pdo = $this->pool ? $this->pool->get() : null;
            if (!$pdo) {
                $response->status(500);
                $response->end(json_encode(["error" => "Database connection failure"]));
                return;
            }

            try {
                if ($path === '/raw/1table') {
                    $stmt = $pdo->query("SELECT id, name, email, phone, city, created_at FROM customer LIMIT 100");
                    $rows = $stmt->fetchAll();
                    $response->end(json_encode($rows));
                } elseif ($path === '/raw/2join') {
                    $stmt = $pdo->query("
                        SELECT o.id, c.name, o.quantity, o.total_amount, o.order_date
                        FROM orders o
                        JOIN customer c ON o.customer_id = c.id
                        LIMIT 100
                    ");
                    $rows = $stmt->fetchAll();
                    $response->end(json_encode($rows));
                } elseif ($path === '/raw/3join') {
                    $stmt = $pdo->query("
                        SELECT o.id, c.name, p.name AS product_name, o.quantity, o.total_amount
                        FROM orders o
                        JOIN customer c ON o.customer_id = c.id
                        JOIN product p ON o.product_id = p.id
                        LIMIT 100
                    ");
                    $rows = $stmt->fetchAll();
                    $response->end(json_encode($rows));
                } elseif ($path === '/raw/4join') {
                    $stmt = $pdo->query("
                        SELECT o.id, c.name, p.name AS product_name, f.name AS factory_name, o.quantity, o.total_amount
                        FROM orders o
                        JOIN customer c ON o.customer_id = c.id
                        JOIN product p ON o.product_id = p.id
                        JOIN factory f ON p.factory_id = f.id
                        LIMIT 100
                    ");
                    $rows = $stmt->fetchAll();
                    $response->end(json_encode($rows));
                } else {
                    $response->status(404);
                    $response->end(json_encode(["error" => "Endpoint not found"]));
                }
            } catch (\Throwable $e) {
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

$app = new BenchmarkGetServer();
$app->run();
