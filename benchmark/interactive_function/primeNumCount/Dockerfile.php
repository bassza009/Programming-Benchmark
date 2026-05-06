FROM php:8.4-cli-alpine
WORKDIR /app
COPY . .
CMD ["php", "prime.php"]
