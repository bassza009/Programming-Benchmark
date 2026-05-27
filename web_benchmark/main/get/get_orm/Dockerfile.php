FROM php:8.3-cli-alpine

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
    mysql-client \
    curl

RUN docker-php-ext-install pdo_mysql && \
    yes "" | pecl install swoole && \
    docker-php-ext-enable swoole

RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
    php composer-setup.php --install-dir=/usr/local/bin --filename=composer && \
    rm composer-setup.php

COPY composer.json .
COPY server.php .

RUN composer install --no-dev --optimize-autoloader

EXPOSE 8003
CMD ["php", "server.php"]
