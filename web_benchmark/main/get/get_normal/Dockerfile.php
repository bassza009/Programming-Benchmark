FROM php:8.2-cli-alpine

WORKDIR /app

RUN apk add --no-cache \
    git \
    autoconf \
    g++ \
    make \
    linux-headers \
    brotli-dev \
    openssl-dev \
    curl-dev \
    mysql-client

    
RUN docker-php-ext-install pdo_mysql && \
    yes "" | pecl install swoole && \
    docker-php-ext-enable swoole

COPY server.php .

EXPOSE 8003
CMD ["php", "server.php"]