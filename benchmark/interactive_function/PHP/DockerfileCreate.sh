docker build -t php83-opcache .

docker run -d \
  --name phpbench \
  -v "$PWD:/app" \
  -w /app \
  php83-opcache \
  sleep infinity
