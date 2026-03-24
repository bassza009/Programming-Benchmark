cat <<EOF > Dockerfile.node
FROM node:20-slim
WORKDIR /app
COPY . .
CMD ["node", "benchmark/door/door.js"]
EOF