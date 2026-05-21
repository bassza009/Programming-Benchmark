FROM openswoole/swoole:php8.2-latest

WORKDIR /app
COPY server.php .

ENV PORT=8003
EXPOSE 8003

CMD ["php", "server.php"]
