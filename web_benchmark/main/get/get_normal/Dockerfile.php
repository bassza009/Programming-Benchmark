FROM php:8.2-cli-alpine

WORKDIR /app

RUN apk add --no-cache git autoconf g++ make mysql-client linux-headers


RUN docker-php-ext-install pdo_mysql && \
    pecl install swoole && \
    docker-php-ext-enable swoole

COPY server.php .

EXPOSE 8003
CMD ["php", "server.php"]