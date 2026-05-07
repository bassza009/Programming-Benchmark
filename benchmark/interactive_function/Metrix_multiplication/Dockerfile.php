FROM php:8.4.2-cli-alpine
WORKDIR /app
COPY . .
CMD ["php", "Metrix.php"]
