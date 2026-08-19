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

        List<Integer> list = jdbcTemplate.query("SELECT 1 FROM users LIMIT 1", (rs, rowNum) -> rs.getInt(1));
        if (list.isEmpty()) {
            seedData();
        }
    }

    private void seedData() {
        List<Object[]> userBatch = new ArrayList<>(10000);
        List<Object[]> profileBatch = new ArrayList<>(10000);
        List<Object[]> orderBatch = new ArrayList<>(10000);
        List<Object[]> itemBatch = new ArrayList<>(5000);

        for (int i = 1; i <= 10000; i++) {
            userBatch.add(new Object[]{"User" + i, "user" + i + "@example.com"});
            profileBatch.add(new Object[]{i, 20 + (i % 50), "Bio " + i, "555-" + i, "Address " + i});
            orderBatch.add(new Object[]{i, 100.0 + i});

            if (i % 10 == 0) {
                for (int j = 0; j < 5; j++) {
                    itemBatch.add(new Object[]{i, "Product" + j, 10.0 + j});
                }
            }
        }

        jdbcTemplate.batchUpdate("INSERT INTO users (name, email) VALUES (?, ?)", userBatch);
        jdbcTemplate.batchUpdate("INSERT INTO profiles (user_id, age, bio, phone, address) VALUES (?, ?, ?, ?, ?)", profileBatch);
        jdbcTemplate.batchUpdate("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", orderBatch);
        if (!itemBatch.isEmpty()) {
            jdbcTemplate.batchUpdate("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)", itemBatch);
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
