FROM openswoole/swoole:php8.4-latest

WORKDIR /app
COPY server.php .

ENV PORT=8003
EXPOSE 8080

CMD ["php", "server.php"]
