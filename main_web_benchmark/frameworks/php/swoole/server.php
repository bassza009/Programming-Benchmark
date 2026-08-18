<?php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;
use Swoole\Database\PDOConfig;
use Swoole\Database\PDOPool;

$dbHost = getenv('DB_HOST') ?: '127.0.0.1';
$dbPort = (int)(getenv('DB_PORT') ?: 3306);
$dbUser = getenv('DB_USER') ?: 'admin';
$dbPass = getenv('DB_PASS') ?: 'secret';
$dbName = getenv('DB_NAME') ?: 'benchmark_db';

$server = new Server("0.0.0.0", 8003);

$server->set([
    'worker_num' => swoole_cpu_num() * 2,
    'enable_coroutine' => true,
    'log_level' => SWOOLE_LOG_ERROR,
    'open_tcp_nodelay' => true,
    'max_coroutine' => 100000,
]);

$pool = null;

$server->on("WorkerStart", function ($server, $workerId) use ($dbHost, $dbPort, $dbUser, $dbPass, $dbName, &$pool) {
    $config = (new PDOConfig())
        ->withHost($dbHost)
        ->withPort($dbPort)
        ->withDbName($dbName)
        ->withCharset('utf8mb4')
        ->withUsername($dbUser)
        ->withPassword($dbPass)
        ->withDriver('mysql')
        ->withOptions([
            \PDO::ATTR_ERRMODE => \PDO::ERRMODE_EXCEPTION,
            \PDO::ATTR_DEFAULT_FETCH_MODE => \PDO::FETCH_ASSOC
        ]);
    $pool = new PDOPool($config, 64);
});

$server->on("Request", function (Request $request, Response $response) use (&$pool) {
    $uri = $request->server['request_uri'];
    $method = $request->server['request_method'];

    $response->header("Content-Type", "application/json");

    if ($uri === '/' && $method === 'GET') {
        $response->end(json_encode(["status" => "success", "language" => "PHP", "framework" => "Swoole", "port" => 8003]));
        return;
    }

    $pdo = $pool->get();
    try {
        if ($method === 'GET') {
            if ($uri === '/raw/1table') {
                $stmt = $pdo->query("SELECT * FROM users LIMIT 100");
                $data = $stmt->fetchAll();
                $response->end(json_encode($data));
            } elseif ($uri === '/raw/2join') {
                $stmt = $pdo->query("SELECT u.name, p.age FROM users u JOIN profiles p ON u.id = p.user_id LIMIT 100");
                $data = $stmt->fetchAll();
                $response->end(json_encode($data));
            } elseif ($uri === '/raw/3join') {
                $stmt = $pdo->query("SELECT u.name, p.age, o.total_amount FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id LIMIT 100");
                $data = $stmt->fetchAll();
                $response->end(json_encode($data));
            } elseif ($uri === '/raw/4join') {
                $stmt = $pdo->query("SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id JOIN order_items oi ON o.id = oi.order_id LIMIT 100");
                $data = $stmt->fetchAll();
                $response->end(json_encode($data));
            } else {
                $response->status(404);
                $response->end(json_encode(["error" => "Not found"]));
            }
        } elseif ($method === 'POST') {
            $randomId = bin2hex(random_bytes(4));
            $email = "php_{$randomId}_" . posix_getpid() . "@example.com";

            if ($uri === '/raw/post/1table') {
                $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
                $stmt->execute(["User_{$randomId}", $email]);
                $userId = $pdo->lastInsertId();
                $response->status(201);
                $response->end(json_encode(["user_id" => (int)$userId]));
            } elseif ($uri === '/raw/post/2table') {
                $pdo->beginTransaction();
                $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
                $stmt->execute(["User_{$randomId}", $email]);
                $userId = $pdo->lastInsertId();
                $stmt2 = $pdo->prepare("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)");
                $stmt2->execute([$userId, 25, "123 Main St", "Bio {$userId}", "555-{$randomId}"]);
                $pdo->commit();
                $response->status(201);
                $response->end(json_encode(["user_id" => (int)$userId]));
            } elseif ($uri === '/raw/post/3table') {
                $pdo->beginTransaction();
                $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
                $stmt->execute(["User_{$randomId}", $email]);
                $userId = $pdo->lastInsertId();
                $stmt2 = $pdo->prepare("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)");
                $stmt2->execute([$userId, 25, "123 Main St", "Bio {$userId}", "555-{$randomId}"]);
                $stmt3 = $pdo->prepare("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)");
                $stmt3->execute([$userId, 100.00]);
                $pdo->commit();
                $response->status(201);
                $response->end(json_encode(["user_id" => (int)$userId]));
            } elseif ($uri === '/raw/post/4table') {
                $pdo->beginTransaction();
                $stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
                $stmt->execute(["User_{$randomId}", $email]);
                $userId = $pdo->lastInsertId();
                $stmt2 = $pdo->prepare("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)");
                $stmt2->execute([$userId, 25, "123 Main St", "Bio {$userId}", "555-{$randomId}"]);
                $stmt3 = $pdo->prepare("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)");
                $stmt3->execute([$userId, 100.00]);
                $orderId = $pdo->lastInsertId();
                $stmt4 = $pdo->prepare("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)");
                $stmt4->execute([$orderId, "Item1_{$randomId}", 25.00]);
                $stmt4->execute([$orderId, "Item2_{$randomId}", 75.00]);
                $pdo->commit();
                $response->status(201);
                $response->end(json_encode(["user_id" => (int)$userId]));
            } else {
                $response->status(404);
                $response->end(json_encode(["error" => "Not found"]));
            }
        }
    } catch (\Throwable $e) {
        if ($pdo->inTransaction()) {
            $pdo->rollBack();
        }
        $response->status(500);
        $response->end(json_encode(["error" => $e->getMessage()]));
    } finally {
        $pool->put($pdo);
    }
});

$server->start();
