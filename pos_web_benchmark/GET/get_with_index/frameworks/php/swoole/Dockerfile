FROM phpswoole/swoole:php8.2-alpine

RUN apk add --no-cache postgresql-dev \
    && docker-php-ext-install pdo pdo_pgsql

WORKDIR /app

COPY server.php ./

EXPOSE 8003

CMD ["php", "server.php"]
