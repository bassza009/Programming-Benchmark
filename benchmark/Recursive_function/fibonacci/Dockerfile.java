FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY fibonacci.java .
RUN javac fibonacci.java
CMD ["java", "fibonacci"]
