FROM php:8.2-cli

WORKDIR /app
COPY server.php .

ENV PORT=8080
EXPOSE 8080

CMD ["php", "-S", "0.0.0.0:8080", "server.php"]
