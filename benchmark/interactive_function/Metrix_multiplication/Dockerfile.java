FROM openjdk:17-slim
WORKDIR /app
COPY . .
CMD ["java","Metrix.java"]