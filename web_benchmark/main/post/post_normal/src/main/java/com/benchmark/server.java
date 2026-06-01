package com.benchmark;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Map;
import java.util.UUID;

import javax.sql.DataSource;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import static org.springframework.web.reactive.function.server.RequestPredicates.POST;
import static org.springframework.web.reactive.function.server.RequestPredicates.GET;
import org.springframework.web.reactive.function.server.RouterFunction;
import static org.springframework.web.reactive.function.server.RouterFunctions.route;
import org.springframework.web.reactive.function.server.ServerResponse;
import static org.springframework.web.reactive.function.server.ServerResponse.ok;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

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
            .andRoute(POST("/raw/post/1table"), req -> handlePost1Table())
            .andRoute(POST("/raw/post/2table"), req -> handlePost2Table())
            .andRoute(POST("/raw/post/3table"), req -> handlePost3Table())
            .andRoute(POST("/raw/post/4table"), req -> handlePost4Table());
    }

    private static Mono<ServerResponse> handlePost1Table() {
        return Mono.fromCallable(() -> {
            String randomId = UUID.randomUUID().toString().substring(0, 8);
            String email = "test_" + randomId + "@example.com";

            try (Connection conn = dataSource.getConnection();
                 PreparedStatement pstmt = conn.prepareStatement("INSERT INTO users (name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS)) {
                pstmt.setString(1, "User_" + randomId);
                pstmt.setString(2, email);
                pstmt.executeUpdate();

                ResultSet rs = pstmt.getGeneratedKeys();
                if (rs.next()) {
                    return rs.getLong(1);
                }
                throw new Exception("Failed to get user_id");
            }
        }).flatMap(userId -> ServerResponse.status(201).bodyValue(Map.of("user_id", userId)))
         .onErrorResume(e -> ServerResponse.status(500).bodyValue(Map.of("error", e.getMessage())))
         .subscribeOn(Schedulers.boundedElastic());
    }

    private static Mono<ServerResponse> handlePost2Table() {
        return Mono.fromCallable(() -> {
            String randomId = UUID.randomUUID().toString().substring(0, 8);
            String email = "test_" + randomId + "@example.com";

            try (Connection conn = dataSource.getConnection()) {
                conn.setAutoCommit(false);
                try (PreparedStatement pstmt = conn.prepareStatement("INSERT INTO users (name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS)) {
                    pstmt.setString(1, "User_" + randomId);
                    pstmt.setString(2, email);
                    pstmt.executeUpdate();

                    ResultSet rs = pstmt.getGeneratedKeys();
                    if (!rs.next()) throw new Exception("Failed to get user_id");
                    long userId = rs.getLong(1);

                    try (PreparedStatement pstmt2 = conn.prepareStatement("INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)")) {
                        pstmt2.setLong(1, userId);
                        pstmt2.setString(2, "Bio for user " + userId);
                        pstmt2.setString(3, "555-" + randomId);
                        pstmt2.executeUpdate();
                    }

                    conn.commit();
                    return userId;
                } catch (Exception e) {
                    conn.rollback();
                    throw e;
                }
            }
        }).flatMap(userId -> ServerResponse.status(201).bodyValue(Map.of("user_id", userId)))
         .onErrorResume(e -> ServerResponse.status(500).bodyValue(Map.of("error", e.getMessage())))
         .subscribeOn(Schedulers.boundedElastic());
    }

    private static Mono<ServerResponse> handlePost3Table() {
        return Mono.fromCallable(() -> {
            String randomId = UUID.randomUUID().toString().substring(0, 8);
            String email = "test_" + randomId + "@example.com";

            try (Connection conn = dataSource.getConnection()) {
                conn.setAutoCommit(false);
                try (PreparedStatement pstmt = conn.prepareStatement("INSERT INTO users (name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS)) {
                    pstmt.setString(1, "User_" + randomId);
                    pstmt.setString(2, email);
                    pstmt.executeUpdate();

                    ResultSet rs = pstmt.getGeneratedKeys();
                    if (!rs.next()) throw new Exception("Failed to get user_id");
                    long userId = rs.getLong(1);

                    try (PreparedStatement pstmt2 = conn.prepareStatement("INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)")) {
                        pstmt2.setLong(1, userId);
                        pstmt2.setString(2, "Bio for user " + userId);
                        pstmt2.setString(3, "555-" + randomId);
                        pstmt2.executeUpdate();
                    }

                    try (PreparedStatement pstmt3 = conn.prepareStatement("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)")) {
                        pstmt3.setLong(1, userId);
                        pstmt3.setDouble(2, 100.00);
                        pstmt3.executeUpdate();
                    }

                    conn.commit();
                    return userId;
                } catch (Exception e) {
                    conn.rollback();
                    throw e;
                }
            }
        }).flatMap(userId -> ServerResponse.status(201).bodyValue(Map.of("user_id", userId)))
         .onErrorResume(e -> ServerResponse.status(500).bodyValue(Map.of("error", e.getMessage())))
         .subscribeOn(Schedulers.boundedElastic());
    }

    private static Mono<ServerResponse> handlePost4Table() {
        return Mono.fromCallable(() -> {
            String randomId = UUID.randomUUID().toString().substring(0, 8);
            String email = "test_" + randomId + "@example.com";

            try (Connection conn = dataSource.getConnection()) {
                conn.setAutoCommit(false);
                try (PreparedStatement pstmt = conn.prepareStatement("INSERT INTO users (name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS)) {
                    pstmt.setString(1, "User_" + randomId);
                    pstmt.setString(2, email);
                    pstmt.executeUpdate();

                    ResultSet rs = pstmt.getGeneratedKeys();
                    if (!rs.next()) throw new Exception("Failed to get user_id");
                    long userId = rs.getLong(1);

                    try (PreparedStatement pstmt2 = conn.prepareStatement("INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)")) {
                        pstmt2.setLong(1, userId);
                        pstmt2.setString(2, "Bio for user " + userId);
                        pstmt2.setString(3, "555-" + randomId);
                        pstmt2.executeUpdate();
                    }

                    long orderId;
                    try (PreparedStatement pstmt3 = conn.prepareStatement("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS)) {
                        pstmt3.setLong(1, userId);
                        pstmt3.setDouble(2, 100.00);
                        pstmt3.executeUpdate();

                        ResultSet rsOrder = pstmt3.getGeneratedKeys();
                        if (!rsOrder.next()) throw new Exception("Failed to get order_id");
                        orderId = rsOrder.getLong(1);
                    }

                    try (PreparedStatement pstmt4 = conn.prepareStatement("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)")) {
                        pstmt4.setLong(1, orderId);
                        pstmt4.setString(2, "Product_" + randomId + "_1");
                        pstmt4.setDouble(3, 25.00);
                        pstmt4.executeUpdate();

                        pstmt4.setLong(1, orderId);
                        pstmt4.setString(2, "Product_" + randomId + "_2");
                        pstmt4.setDouble(3, 75.00);
                        pstmt4.executeUpdate();
                    }

                    conn.commit();
                    return userId;
                } catch (Exception e) {
                    conn.rollback();
                    throw e;
                }
            }
        }).flatMap(userId -> ServerResponse.status(201).bodyValue(Map.of("user_id", userId)))
         .onErrorResume(e -> ServerResponse.status(500).bodyValue(Map.of("error", e.getMessage())))
         .subscribeOn(Schedulers.boundedElastic());
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

            stmt.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100) UNIQUE)");
            stmt.execute("CREATE TABLE IF NOT EXISTS profiles (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, bio VARCHAR(255), phone VARCHAR(20))");
            stmt.execute("CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, total_amount DECIMAL(10, 2))");
            stmt.execute("CREATE TABLE IF NOT EXISTS order_items (id INT AUTO_INCREMENT PRIMARY KEY, order_id INT, product_name VARCHAR(100), price DECIMAL(10, 2))");
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
