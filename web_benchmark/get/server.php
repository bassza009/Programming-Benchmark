<?php
/**
 * Simple GET HTTP server for benchmarking in PHP
 * Run with: php -S localhost:8080 server.php
 */

$port = $_ENV['PORT'] ?? 8080;

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['error' => 'Method Not Allowed']);
    exit;
}

header('Content-Type: application/json');

$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($path === '/' || $path === '') {
    echo json_encode([
        'status' => 'ok',
        'message' => 'Hello from PHP GET Server',
        'language' => 'PHP'
    ]);
} elseif ($path === '/health') {
    echo json_encode(['status' => 'healthy']);
} elseif (strpos($path, '/api/data') === 0) {
    echo json_encode([
        'data' => 'benchmark_data',
        'timestamp' => 1234567890,
        'value' => 42
    ]);
} else {
    http_response_code(404);
    echo json_encode(['error' => 'Not found']);
}
?>
