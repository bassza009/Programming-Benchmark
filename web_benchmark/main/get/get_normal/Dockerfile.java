FROM maven:3.8-openjdk-17

WORKDIR /app

COPY pom.xml .
COPY Server.java src/main/java/com/benchmark/

RUN mvn clean package -DskipTests -q

EXPOSE 8005
CMD ["java", "-jar", "target/benchmark-0.0.1-SNAPSHOT.jar"]
