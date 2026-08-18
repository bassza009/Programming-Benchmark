package com.example.benchmark;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.transaction.annotation.Transactional;

import jakarta.annotation.PostConstruct;
import java.sql.PreparedStatement;
import java.sql.Statement;
import java.util.*;

@SpringBootApplication
@RestController
public class BenchmarkApplication {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public static void main(String[] args) {
        System.setProperty("server.port", "8005");
        SpringApplication.run(BenchmarkApplication.class, args);
    }

    @PostConstruct
    public void initSchema() {
        jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS users (" +
                "id INT AUTO_INCREMENT PRIMARY KEY, " +
                "name VARCHAR(100), " +
                "email VARCHAR(100) UNIQUE)");

        jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS profiles (" +
                "id INT AUTO_INCREMENT PRIMARY KEY, " +
                "user_id INT, " +
                "age INT, " +
                "bio VARCHAR(255), " +
                "phone VARCHAR(20), " +
                "address VARCHAR(255))");

        jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS orders (" +
                "id INT AUTO_INCREMENT PRIMARY KEY, " +
                "user_id INT, " +
                "total_amount DECIMAL(10, 2))");

        jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS order_items (" +
                "id INT AUTO_INCREMENT PRIMARY KEY, " +
                "order_id INT, " +
                "product_name VARCHAR(100), " +
                "price DECIMAL(10, 2))");
    }

    @GetMapping("/")
    public Map<String, String> root() {
        Map<String, String> res = new HashMap<>();
        res.put("status", "success");
        res.put("message", "Java Spring Boot POST Benchmark");
        return res;
    }

    @PostMapping("/raw/post/1table")
    public ResponseEntity<?> post1Table() {
        try {
            String randId = UUID.randomUUID().toString().substring(0, 8);
            String email = "java_test_" + randId + "_" + System.nanoTime() + "@example.com";
            KeyHolder keyHolder = new GeneratedKeyHolder();
            jdbcTemplate.update(connection -> {
                PreparedStatement ps = connection.prepareStatement("INSERT INTO users (name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS);
                ps.setString(1, "User_" + randId);
                ps.setString(2, email);
                return ps;
            }, keyHolder);
            Map<String, Object> body = new HashMap<>();
            body.put("user_id", Objects.requireNonNull(keyHolder.getKey()).longValue());
            return ResponseEntity.status(HttpStatus.CREATED).body(body);
        } catch (Exception e) {
            Map<String, String> err = new HashMap<>();
            err.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
        }
    }

    @PostMapping("/raw/post/2table")
    @Transactional
    public ResponseEntity<?> post2Table() {
        try {
            String randId = UUID.randomUUID().toString().substring(0, 8);
            String email = "java_test_" + randId + "_" + System.nanoTime() + "@example.com";
            KeyHolder keyHolder = new GeneratedKeyHolder();
            jdbcTemplate.update(connection -> {
                PreparedStatement ps = connection.prepareStatement("INSERT INTO users (name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS);
                ps.setString(1, "User_" + randId);
                ps.setString(2, email);
                return ps;
            }, keyHolder);
            long userId = Objects.requireNonNull(keyHolder.getKey()).longValue();

            jdbcTemplate.update("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)", userId, 25, "123 St", "Bio " + userId, "555-" + randId);

            Map<String, Object> body = new HashMap<>();
            body.put("user_id", userId);
            return ResponseEntity.status(HttpStatus.CREATED).body(body);
        } catch (Exception e) {
            Map<String, String> err = new HashMap<>();
            err.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
        }
    }

    @PostMapping("/raw/post/3table")
    @Transactional
    public ResponseEntity<?> post3Table() {
        try {
            String randId = UUID.randomUUID().toString().substring(0, 8);
            String email = "java_test_" + randId + "_" + System.nanoTime() + "@example.com";
            KeyHolder keyHolder = new GeneratedKeyHolder();
            jdbcTemplate.update(connection -> {
                PreparedStatement ps = connection.prepareStatement("INSERT INTO users (name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS);
                ps.setString(1, "User_" + randId);
                ps.setString(2, email);
                return ps;
            }, keyHolder);
            long userId = Objects.requireNonNull(keyHolder.getKey()).longValue();

            jdbcTemplate.update("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)", userId, 25, "123 St", "Bio " + userId, "555-" + randId);
            jdbcTemplate.update("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", userId, 100.00);

            Map<String, Object> body = new HashMap<>();
            body.put("user_id", userId);
            return ResponseEntity.status(HttpStatus.CREATED).body(body);
        } catch (Exception e) {
            Map<String, String> err = new HashMap<>();
            err.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
        }
    }

    @PostMapping("/raw/post/4table")
    @Transactional
    public ResponseEntity<?> post4Table() {
        try {
            String randId = UUID.randomUUID().toString().substring(0, 8);
            String email = "java_test_" + randId + "_" + System.nanoTime() + "@example.com";
            KeyHolder userKeyHolder = new GeneratedKeyHolder();
            jdbcTemplate.update(connection -> {
                PreparedStatement ps = connection.prepareStatement("INSERT INTO users (name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS);
                ps.setString(1, "User_" + randId);
                ps.setString(2, email);
                return ps;
            }, userKeyHolder);
            long userId = Objects.requireNonNull(userKeyHolder.getKey()).longValue();

            jdbcTemplate.update("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)", userId, 25, "123 St", "Bio " + userId, "555-" + randId);

            KeyHolder orderKeyHolder = new GeneratedKeyHolder();
            jdbcTemplate.update(connection -> {
                PreparedStatement ps = connection.prepareStatement("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS);
                ps.setLong(1, userId);
                ps.setDouble(2, 100.00);
                return ps;
            }, orderKeyHolder);
            long orderId = Objects.requireNonNull(orderKeyHolder.getKey()).longValue();

            jdbcTemplate.update("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)", orderId, "Prod1_" + randId, 25.00);
            jdbcTemplate.update("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)", orderId, "Prod2_" + randId, 75.00);

            Map<String, Object> body = new HashMap<>();
            body.put("user_id", userId);
            return ResponseEntity.status(HttpStatus.CREATED).body(body);
        } catch (Exception e) {
            Map<String, String> err = new HashMap<>();
            err.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
        }
    }
}
