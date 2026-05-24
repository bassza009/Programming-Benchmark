package com.benchmark;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono; // 💡 เปลี่ยนจาก Flux เป็น Mono
import reactor.core.scheduler.Schedulers;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import static org.springframework.web.reactive.function.server.RequestPredicates.*;
import static org.springframework.web.reactive.function.server.RouterFunctions.route;
import static org.springframework.web.reactive.function.server.ServerResponse.ok;

@SpringBootApplication
public class server {
    private static DataSource dataSource;

    public static void main(String[] args) {
        System.setProperty("server.port", "8005");
        initDatabase();
        SpringApplication.run(server.class, args);
    }

    @Bean
    public RouterFunction<ServerResponse> routes() {
        return route(GET("/"), req -> ok().bodyValue(Map.of("status", "success", "message", "Hello Benchmark")))
            .andRoute(GET("/raw/1table"), req -> ok().body(query1Table(), List.class))
            .andRoute(GET("/raw/2join"), req -> ok().body(query2Join(), List.class))
            .andRoute(GET("/raw/3join"), req -> ok().body(query3Join(), List.class))
            .andRoute(GET("/raw/4join"), req -> ok().body(query4Join(), List.class));
    }

    // 💡 เปลี่ยนจาก Flux เป็น Mono ทั้งหมด
    private static Mono<List<?>> query1Table() {
        return Mono.fromCallable(() -> {
            List<Map<String, Object>> results = new LinkedList<>();
            try (Connection conn = dataSource.getConnection();
                 Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery("SELECT * FROM users LIMIT 100")) {
                while (rs.next()) {
                    Map<String, Object> row = new HashMap<>();
                    row.put("id", rs.getInt("id"));
                    row.put("name", rs.getString("name"));
                    row.put("email", rs.getString("email"));
                    results.add(row);
                }
            }
            return results;
        }).subscribeOn(Schedulers.boundedElastic());
    }

    private static Mono<List<?>> query2Join() {
        return Mono.fromCallable(() -> {
            List<Map<String, Object>> results = new LinkedList<>();
            try (Connection conn = dataSource.getConnection();
                 Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery("SELECT u.name, p.age FROM users u JOIN profiles p ON u.id = p.user_id LIMIT 100")) {
                while (rs.next()) {
                    Map<String, Object> row = new HashMap<>();
                    row.put("name", rs.getString("name"));
                    row.put("age", rs.getInt("age"));
                    results.add(row);
                }
            }
            return results;
        }).subscribeOn(Schedulers.boundedElastic());
    }

    private static Mono<List<?>> query3Join() {
        return Mono.fromCallable(() -> {
            List<Map<String, Object>> results = new LinkedList<>();
            try (Connection conn = dataSource.getConnection();
                 Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery("SELECT u.name, p.age, o.total_amount FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id LIMIT 100")) {
                while (rs.next()) {
                    Map<String, Object> row = new HashMap<>();
                    row.put("name", rs.getString("name"));
                    row.put("age", rs.getInt("age"));
                    row.put("total_amount", rs.getDouble("total_amount"));
                    results.add(row);
                }
            }
            return results;
        }).subscribeOn(Schedulers.boundedElastic());
    }

    private static Mono<List<?>> query4Join() {
        return Mono.fromCallable(() -> {
            List<Map<String, Object>> results = new LinkedList<>();
            try (Connection conn = dataSource.getConnection();
                 Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery("SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id JOIN order_items oi ON o.id = oi.order_id LIMIT 100")) {
                while (rs.next()) {
                    Map<String, Object> row = new HashMap<>();
                    row.put("name", rs.getString("name"));
                    row.put("age", rs.getInt("age"));
                    row.put("total_amount", rs.getDouble("total_amount"));
                    row.put("product_name", rs.getString("product_name"));
                    results.add(row);
                }
            }
            return results;
        }).subscribeOn(Schedulers.boundedElastic());
    }

    private static void initDatabase() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:mysql://127.0.0.1:3306/benchmark_db");
        config.setUsername("admin");
        config.setPassword("secret");
        config.setMaximumPoolSize(100);
        config.setMinimumIdle(10);
        dataSource = new HikariDataSource(config);

        try (Connection conn = dataSource.getConnection();
             Statement stmt = conn.createStatement()) {

            stmt.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100))");
            stmt.execute("CREATE TABLE IF NOT EXISTS profiles (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, age INT, address VARCHAR(255))");
            stmt.execute("CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, total_amount DECIMAL(10, 2))");
            stmt.execute("CREATE TABLE IF NOT EXISTS order_items (id INT AUTO_INCREMENT PRIMARY KEY, order_id INT, product_name VARCHAR(100), price DECIMAL(10, 2))");

            ResultSet rs = stmt.executeQuery("SELECT COUNT(*) FROM users");
            if (rs.next() && rs.getInt(1) == 0) {
                insertMockData(conn);
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static void insertMockData(Connection conn) throws Exception {
        for (int i = 1; i <= 10000; i++) {
            try (Statement stmt = conn.createStatement()) {
                stmt.execute("INSERT INTO users (name, email) VALUES ('User" + i + "', 'user" + i + "@example.com')");
                stmt.execute("INSERT INTO profiles (user_id, age, address) VALUES (" + i + ", " + (20 + i % 50) + ", 'Address " + i + "')");
                stmt.execute("INSERT INTO orders (user_id, total_amount) VALUES (" + i + ", " + (100.0 + i) + ")");

                if (i % 10 == 0) {
                    for (int j = 0; j < 5; j++) {
                        stmt.execute("INSERT INTO order_items (order_id, product_name, price) VALUES (" + i + ", 'Product" + j + "', " + (10.0 + j) + ")");
                    }
                }
            }
        }
    }
}