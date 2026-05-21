FROM openswoole/swoole:22.1.2-php8.4

WORKDIR /app
COPY server.php .

ENV PORT=8003
EXPOSE 8080

CMD ["php", "server.php"]
