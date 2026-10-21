FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY Metrix.java .
RUN javac Metrix.java
CMD ["java", "Metrix"]
