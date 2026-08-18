# Java Spring Boot Benchmark Server

* **Language**: Java (JDK 21)
* **Framework**: Spring Boot 3 (`JdbcTemplate` + `HikariCP`)
* **Database Driver**: `mysql-connector-j`
* **Default Port**: `8005`

## Running Locally (Bare Metal)
```bash
mvn clean package -DskipTests
java -jar target/benchmark-springboot-1.0.0.jar
```

## Running with Docker
```bash
docker build -t benchmark-springboot .
docker run -p 8005:8005 -e DB_HOST=host.docker.internal benchmark-springboot
```
