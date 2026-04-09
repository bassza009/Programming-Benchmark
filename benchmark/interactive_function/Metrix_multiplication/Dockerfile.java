FROM eclipse-temurin:17-jdk-focal
WORKDIR /app
COPY . .
CMD ["java","Metrix.java"]