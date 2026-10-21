FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY bubble.java .
RUN javac bubble.java
CMD ["java", "bubble"]
