FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY prime.java .
RUN javac prime.java
CMD ["java", "prime"]
