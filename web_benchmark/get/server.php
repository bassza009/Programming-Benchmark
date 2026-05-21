<?php
/**
 * Concurrent GET HTTP server for benchmarking in PHP using Swoole
 */
use Swoole\HTTP\Server;

$port = (int)($_ENV['PORT'] ?? 8003);
$server = new Server("0.0.0.0", $port);

// 🚀 ปลดล็อคพลัง Swoole: สั่งให้สร้าง Worker เท่ากับจำนวน Core CPU x 2 (เพื่อความแฟร์!)
$server->set([
    'worker_num' => swoole_cpu_num() * 2,
]);

$server->on("request", function ($request, $response) {
    // 💡 Swoole ต้องใช้คีย์ตัวพิมพ์เล็ก (request_method, request_uri)
    $method = $request->server['request_method'] ?? '';
    $path = $request->server['request_uri'] ?? '/';

    if ($method !== 'GET') {
        $response->setStatusCode(405);
        $response->header('Content-Type', 'application/json');
        $response->end(json_encode(['error' => 'Method Not Allowed']));
        return;
    }

    $response->header('Content-Type', 'application/json');

    if ($path === '/' || $path === '') {
        $response->end(json_encode([
            'status' => 'ok',
            'message' => 'Hello from PHP GET Server',
            'language' => 'PHP'
        ]));
    } elseif ($path === '/health') {
        $response->end(json_encode(['status' => 'healthy']));
    } elseif (strpos($path, '/api/data') === 0) {
        $response->end(json_encode([
            'data' => 'benchmark_data',
            'timestamp' => 1234567890,
            'value' => 42
        ]));
    } else {
        $response->setStatusCode(404);
        $response->end(json_encode(['error' => 'Not found']));
    }
});

echo "Swoole HTTP Server running on 0.0.0.0:" . $port . " with " . (swoole_cpu_num() * 2) . " workers\n";
$server->start();
?>