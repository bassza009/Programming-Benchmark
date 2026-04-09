FROM openjdk:17-slim
WORKDIR /app
COPY . .
CMD ["java","door.java"]