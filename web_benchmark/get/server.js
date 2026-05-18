#!/usr/bin/env node
/**
 * Simple GET HTTP server for benchmarking in Node.js
 */

const http = require('http');
const url = require('url');

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;

    if (req.method !== 'GET') {
        res.writeHead(405, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Method Not Allowed' }));
        return;
    }

    res.writeHead(200, { 'Content-Type': 'application/json' });

    if (pathname === '/') {
        res.end(JSON.stringify({
            status: 'ok',
            message: 'Hello from Node.js GET Server',
            language: 'Node.js'
        }));
    } else if (pathname === '/health') {
        res.end(JSON.stringify({ status: 'healthy' }));
    } else if (pathname.startsWith('/api/data')) {
        res.end(JSON.stringify({
            data: 'benchmark_data',
            timestamp: 1234567890,
            value: 42
        }));
    } else {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not found' }));
    }
});

server.listen(PORT, () => {
    console.error(`Node.js GET Server running on port ${PORT}`);
});

server.on('error', (err) => {
    console.error('Server error:', err);
    process.exit(1);
});
