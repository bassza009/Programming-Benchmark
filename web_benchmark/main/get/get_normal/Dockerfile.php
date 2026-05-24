FROM php:8.2-cli-alpine

WORKDIR /app

RUN apk add --no-cache git autoconf g++ make mysql-client

RUN pecl install swoole pdo_mysql && \
    docker-php-ext-enable swoole pdo_mysql

COPY server.php .

EXPOSE 8080
CMD ["php", "server.php"]
