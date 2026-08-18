FROM phpswoole/swoole:php8.2-alpine

WORKDIR /var/www

RUN docker-php-ext-install pdo pdo_mysql

COPY server.php .

EXPOSE 8003

CMD ["php", "server.php"]
