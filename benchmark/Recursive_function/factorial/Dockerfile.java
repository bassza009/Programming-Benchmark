FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY factorial.java .
RUN javac factorial.java
CMD ["java", "factorial"]
