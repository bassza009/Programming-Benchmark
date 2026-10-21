FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY door.java .
RUN javac door.java
CMD ["java", "door"]
