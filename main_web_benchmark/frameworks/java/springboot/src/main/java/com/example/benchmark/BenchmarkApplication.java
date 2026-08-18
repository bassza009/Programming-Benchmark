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

    // ==================== Health Check ====================
    @GetMapping("/")
    public Map<String, Object> root() {
        Map<String, Object> res = new HashMap<>();
        res.put("status", "success");
        res.put("language", "Java");
        res.put("framework", "Spring Boot");
        res.put("port", 8005);
        return res;
    }

    // ==================== GET (Read) Endpoints ====================
    @GetMapping("/raw/1table")
    public List<Map<String, Object>> get1Table() {
        return jdbcTemplate.queryForList("SELECT * FROM users LIMIT 100");
    }

    @GetMapping("/raw/2join")
    public List<Map<String, Object>> get2Join() {
        return jdbcTemplate.queryForList(
            "SELECT u.name, p.age FROM users u " +
            "JOIN profiles p ON u.id = p.user_id LIMIT 100"
        );
    }

    @GetMapping("/raw/3join")
    public List<Map<String, Object>> get3Join() {
        return jdbcTemplate.queryForList(
            "SELECT u.name, p.age, o.total_amount FROM users u " +
            "JOIN profiles p ON u.id = p.user_id " +
            "JOIN orders o ON u.id = o.user_id LIMIT 100"
        );
    }

    @GetMapping("/raw/4join")
    public List<Map<String, Object>> get4Join() {
        return jdbcTemplate.queryForList(
            "SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u " +
            "JOIN profiles p ON u.id = p.user_id " +
            "JOIN orders o ON u.id = o.user_id " +
            "JOIN order_items oi ON o.id = oi.order_id LIMIT 100"
        );
    }

    // ==================== POST (Write / Transaction) Endpoints ====================
    @PostMapping("/raw/post/1table")
    public ResponseEntity<Map<String, Object>> post1Table() {
        try {
            String randomId = UUID.randomUUID().toString().substring(0, 8);
            String email = "java_" + randomId + "_" + Thread.currentThread().getId() + "@example.com";
            KeyHolder keyHolder = new GeneratedKeyHolder();
            jdbcTemplate.update(connection -> {
                PreparedStatement ps = connection.prepareStatement(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    Statement.RETURN_GENERATED_KEYS
                );
                ps.setString(1, "User_" + randomId);
                ps.setString(2, email);
                return ps;
            }, keyHolder);

            Number key = keyHolder.getKey();
            Map<String, Object> resp = new HashMap<>();
            resp.put("user_id", key != null ? key.longValue() : 0);
            return ResponseEntity.status(HttpStatus.CREATED).body(resp);
        } catch (Exception e) {
            Map<String, Object> err = new HashMap<>();
            err.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
        }
    }

    @PostMapping("/raw/post/2table")
    @Transactional
    public ResponseEntity<Map<String, Object>> post2Table() {
        try {
            String randomId = UUID.randomUUID().toString().substring(0, 8);
            String email = "java_" + randomId + "_" + Thread.currentThread().getId() + "@example.com";
            KeyHolder keyHolder = new GeneratedKeyHolder();
            jdbcTemplate.update(connection -> {
                PreparedStatement ps = connection.prepareStatement(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    Statement.RETURN_GENERATED_KEYS
                );
                ps.setString(1, "User_" + randomId);
                ps.setString(2, email);
                return ps;
            }, keyHolder);

            long userId = Objects.requireNonNull(keyHolder.getKey()).longValue();
            jdbcTemplate.update(
                "INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)",
                userId, 25, "123 Main St", "Bio " + userId, "555-" + randomId
            );

            Map<String, Object> resp = new HashMap<>();
            resp.put("user_id", userId);
            return ResponseEntity.status(HttpStatus.CREATED).body(resp);
        } catch (Exception e) {
            Map<String, Object> err = new HashMap<>();
            err.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
        }
    }

    @PostMapping("/raw/post/3table")
    @Transactional
    public ResponseEntity<Map<String, Object>> post3Table() {
        try {
            String randomId = UUID.randomUUID().toString().substring(0, 8);
            String email = "java_" + randomId + "_" + Thread.currentThread().getId() + "@example.com";
            KeyHolder keyHolder = new GeneratedKeyHolder();
            jdbcTemplate.update(connection -> {
                PreparedStatement ps = connection.prepareStatement(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    Statement.RETURN_GENERATED_KEYS
                );
                ps.setString(1, "User_" + randomId);
                ps.setString(2, email);
                return ps;
            }, keyHolder);

            long userId = Objects.requireNonNull(keyHolder.getKey()).longValue();
            jdbcTemplate.update(
                "INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)",
                userId, 25, "123 Main St", "Bio " + userId, "555-" + randomId
            );
            jdbcTemplate.update(
                "INSERT INTO orders (user_id, total_amount) VALUES (?, ?)",
                userId, 100.00
            );

            Map<String, Object> resp = new HashMap<>();
            resp.put("user_id", userId);
            return ResponseEntity.status(HttpStatus.CREATED).body(resp);
        } catch (Exception e) {
            Map<String, Object> err = new HashMap<>();
            err.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
        }
    }

    @PostMapping("/raw/post/4table")
    @Transactional
    public ResponseEntity<Map<String, Object>> post4Table() {
        try {
            String randomId = UUID.randomUUID().toString().substring(0, 8);
            String email = "java_" + randomId + "_" + Thread.currentThread().getId() + "@example.com";
            KeyHolder keyHolder = new GeneratedKeyHolder();
            jdbcTemplate.update(connection -> {
                PreparedStatement ps = connection.prepareStatement(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    Statement.RETURN_GENERATED_KEYS
                );
                ps.setString(1, "User_" + randomId);
                ps.setString(2, email);
                return ps;
            }, keyHolder);

            long userId = Objects.requireNonNull(keyHolder.getKey()).longValue();
            jdbcTemplate.update(
                "INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)",
                userId, 25, "123 Main St", "Bio " + userId, "555-" + randomId
            );

            KeyHolder orderKeyHolder = new GeneratedKeyHolder();
            jdbcTemplate.update(connection -> {
                PreparedStatement ps = connection.prepareStatement(
                    "INSERT INTO orders (user_id, total_amount) VALUES (?, ?)",
                    Statement.RETURN_GENERATED_KEYS
                );
                ps.setLong(1, userId);
                ps.setDouble(2, 100.00);
                return ps;
            }, orderKeyHolder);
            long orderId = Objects.requireNonNull(orderKeyHolder.getKey()).longValue();

            jdbcTemplate.update(
                "INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)",
                orderId, "Item1_" + randomId, 25.00
            );
            jdbcTemplate.update(
                "INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)",
                orderId, "Item2_" + randomId, 75.00
            );

            Map<String, Object> resp = new HashMap<>();
            resp.put("user_id", userId);
            return ResponseEntity.status(HttpStatus.CREATED).body(resp);
        } catch (Exception e) {
            Map<String, Object> err = new HashMap<>();
            err.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
        }
    }
}
