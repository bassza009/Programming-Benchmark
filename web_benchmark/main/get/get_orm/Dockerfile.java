FROM maven:3.8-openjdk-17

WORKDIR /app

COPY pom.xml .
COPY src_java/main/java /app/src/main/java
COPY src_java/main/resources /app/src/main/resources

RUN mvn clean package -DskipTests -q

EXPOSE 8005

CMD ["sh", "-c", "java -jar target/*.jar"]
