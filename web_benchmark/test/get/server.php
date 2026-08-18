<?php
/**
 * Concurrent GET HTTP server for benchmarking in PHP using Swoole
 */
use Swoole\HTTP\Server;

$port = (int)($_ENV['PORT'] ?? 8003);
$server = new Server("0.0.0.0", $port);

//  ระบบหา CPU Core แบบถึกทน 100% (ใช้คำสั่ง nproc ของ Linux แทน)
$cpu_cores = (int)shell_exec('nproc');
if ($cpu_cores < 1) {
    $cpu_cores = 4; // ถ้าหาไม่เจอ ให้ตั้งค่าพื้นฐานไว้ที่ 4 คอร์
}

$server->set([
    'worker_num' => $cpu_cores * 2,
]);

$server->on("request", function ($request, $response) {
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

echo "Swoole HTTP Server running on 0.0.0.0:" . $port . " with " . ($cpu_cores * 2) . " workers\n";
$server->start();
?>