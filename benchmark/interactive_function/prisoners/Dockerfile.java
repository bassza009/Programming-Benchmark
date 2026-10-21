FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY prisoners.java .
RUN javac prisoners.java
CMD ["java", "prisoners"]
