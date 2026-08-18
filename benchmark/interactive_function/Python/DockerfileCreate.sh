#!/usr/bin/env bash
set -e

IMAGE_NAME="python-bench"
CONTAINER_NAME="pythonbench"

docker build -t "$IMAGE_NAME" .

docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

docker run -d \
  --name "$CONTAINER_NAME" \
  --ulimit stack=67108864 \
  -v "$PWD:/app" \
  -w /app \
  "$IMAGE_NAME" \
  sleep infinity

echo "Container started: $CONTAINER_NAME"
echo ""
echo "To enter the container, run:"
echo "docker exec -it $CONTAINER_NAME bash"
