package com.example.benchmark;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;

import jakarta.annotation.PostConstruct;
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
                "email VARCHAR(100))");

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

        Integer count = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM users", Integer.class);
        if (count != null && count == 0) {
            seedData();
        }
    }

    private void seedData() {
        for (int i = 1; i <= 10000; i++) {
            jdbcTemplate.update("INSERT INTO users (name, email) VALUES (?, ?)", "User" + i, "user" + i + "@example.com");
            jdbcTemplate.update("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)", i, 20 + (i % 50), "Address " + i, "Bio " + i, "555-" + i);
            jdbcTemplate.update("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", i, 100.0 + i);

            if (i % 10 == 0) {
                for (int j = 0; j < 5; j++) {
                    jdbcTemplate.update("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)", i, "Product" + j, 10.0 + j);
                }
            }
        }
    }

    @GetMapping("/")
    public Map<String, String> root() {
        Map<String, String> res = new HashMap<>();
        res.put("status", "success");
        res.put("message", "Java Spring Boot GET No-Index Benchmark");
        return res;
    }

    @GetMapping("/raw/1table")
    public List<Map<String, Object>> get1Table() {
        return jdbcTemplate.queryForList("SELECT * FROM users LIMIT 100");
    }

    @GetMapping("/raw/2join")
    public List<Map<String, Object>> get2Join() {
        return jdbcTemplate.queryForList("SELECT u.name, p.age FROM users u JOIN profiles p ON u.id = p.user_id LIMIT 100");
    }

    @GetMapping("/raw/3join")
    public List<Map<String, Object>> get3Join() {
        return jdbcTemplate.queryForList("SELECT u.name, p.age, o.total_amount FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id LIMIT 100");
    }

    @GetMapping("/raw/4join")
    public List<Map<String, Object>> get4Join() {
        return jdbcTemplate.queryForList("SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id JOIN order_items oi ON o.id = oi.order_id LIMIT 100");
    }
}
