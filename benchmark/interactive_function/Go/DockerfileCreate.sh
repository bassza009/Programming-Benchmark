#!/usr/bin/env bash
set -e

IMAGE_NAME="go-bench"
CONTAINER_NAME="gobench"

docker build -t "$IMAGE_NAME" .

# Remove old container if it already exists
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

docker run -d \
  --name "$CONTAINER_NAME" \
  -v "$PWD:/app" \
  -w /app \
  "$IMAGE_NAME" \
  sleep infinity

echo "Container started: $CONTAINER_NAME"
echo ""
echo "To enter the container, run:"
echo "docker exec -it $CONTAINER_NAME bash"
