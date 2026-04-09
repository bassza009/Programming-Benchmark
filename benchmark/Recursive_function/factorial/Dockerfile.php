FROM php:8.3-cli-alpine
WORKDIR /app
COPY . .
CMD ["php", "factorial.php"]
