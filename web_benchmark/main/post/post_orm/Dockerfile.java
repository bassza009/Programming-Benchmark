FROM maven:3.8-openjdk-17

WORKDIR /app

COPY pom.xml .
COPY src/main/java /app/src/main/java


RUN mvn clean package -DskipTests -q

EXPOSE 8005

CMD ["sh", "-c", "java -jar target/*.jar"]
