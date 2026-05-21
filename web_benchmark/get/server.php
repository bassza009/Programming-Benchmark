<?php
/**
 * Concurrent GET HTTP server for benchmarking in PHP using Swoole
 * Runs with Swoole HTTP Server for true concurrency
 */

use Swoole\HTTP\Server;

$port = (int)($_ENV['PORT'] ?? 8003);

$server = new Server("0.0.0.0", $port);

$server->on("request", function ($request, $response) {
    if ($request->server['request_method'] !== 'GET') {
        $response->setStatusCode(405);
        $response->header('Content-Type', 'application/json');
        $response->end(json_encode(['error' => 'Method Not Allowed']));
        return;
    }

    $response->header('Content-Type', 'application/json');

    $path = $request->server['request_uri'];

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

echo "Swoole HTTP Server running on 0.0.0.0:" . $port . "\n";
$server->start();
?>
