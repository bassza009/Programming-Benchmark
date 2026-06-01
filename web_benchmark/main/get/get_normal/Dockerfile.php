FROM php:8.2-cli-alpine

WORKDIR /app

RUN apk add --no-cache autoconf build-base linux-headers brotli-dev openssl-dev curl-dev pkgconfig

RUN pecl install swoole && docker-php-ext-enable swoole

RUN docker-php-ext-install pdo_mysql

COPY server.php .

EXPOSE 8003
CMD ["php", "server.php"]
