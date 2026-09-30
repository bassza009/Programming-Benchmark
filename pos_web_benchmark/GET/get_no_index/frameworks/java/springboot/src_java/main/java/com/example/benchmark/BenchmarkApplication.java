package com.example.benchmark;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;

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

    @GetMapping("/")
    public Map<String, String> root() {
        Map<String, String> res = new HashMap<>();
        res.put("status", "success");
        res.put("message", "Java Spring Boot PostgreSQL GET Benchmark");
        return res;
    }

    @GetMapping("/raw/1table")
    public List<Map<String, Object>> get1Table() {
        return jdbcTemplate.queryForList("SELECT id, name, email, phone, city, created_at FROM customer LIMIT 100");
    }

    @GetMapping("/raw/2join")
    public List<Map<String, Object>> get2Join() {
        return jdbcTemplate.queryForList("SELECT o.id, c.name, o.quantity, o.total_amount, o.order_date FROM orders o JOIN customer c ON o.customer_id = c.id LIMIT 100");
    }

    @GetMapping("/raw/3join")
    public List<Map<String, Object>> get3Join() {
        return jdbcTemplate.queryForList("SELECT o.id, c.name, p.name AS product_name, o.quantity, o.total_amount FROM orders o JOIN customer c ON o.customer_id = c.id JOIN product p ON o.product_id = p.id LIMIT 100");
    }

    @GetMapping("/raw/4join")
    public List<Map<String, Object>> get4Join() {
        return jdbcTemplate.queryForList("SELECT o.id, c.name, p.name AS product_name, f.name AS factory_name, o.quantity, o.total_amount FROM orders o JOIN customer c ON o.customer_id = c.id JOIN product p ON o.product_id = p.id JOIN factory f ON p.factory_id = f.id LIMIT 100");
    }
}
