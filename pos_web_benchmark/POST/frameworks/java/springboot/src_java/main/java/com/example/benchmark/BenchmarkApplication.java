package com.example.benchmark;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.http.HttpStatus;

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
        res.put("message", "Java Spring Boot PostgreSQL POST Benchmark");
        return res;
    }

    @PostMapping("/raw/post/1table")
    @ResponseStatus(HttpStatus.CREATED)
    public Map<String, Object> post1Table() {
        String uid = UUID.randomUUID().toString().substring(0, 8);
        String email = "java_" + uid + "_" + System.nanoTime() + "@example.com";
        Integer customerId = jdbcTemplate.queryForObject(
            "INSERT INTO customer (name, email, phone, city) VALUES (?, ?, ?, ?) RETURNING id",
            Integer.class,
            "Customer_" + uid, email, "555-" + uid, "Benchmark City"
        );
        Map<String, Object> res = new HashMap<>();
        res.put("customer_id", customerId);
        return res;
    }

    @PostMapping("/raw/post/2table")
    @ResponseStatus(HttpStatus.CREATED)
    @Transactional
    public Map<String, Object> post2Table() {
        String uid = UUID.randomUUID().toString().substring(0, 8);
        String email = "java_" + uid + "_" + System.nanoTime() + "@example.com";
        Integer customerId = jdbcTemplate.queryForObject(
            "INSERT INTO customer (name, email, phone, city) VALUES (?, ?, ?, ?) RETURNING id",
            Integer.class,
            "Customer_" + uid, email, "555-" + uid, "Benchmark City"
        );
        Long orderId = jdbcTemplate.queryForObject(
            "INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES (?, 1, 2, 150.00, 'COMPLETED') RETURNING id",
            Long.class,
            customerId
        );
        Map<String, Object> res = new HashMap<>();
        res.put("customer_id", customerId);
        res.put("order_id", orderId);
        return res;
    }

    @PostMapping("/raw/post/3table")
    @ResponseStatus(HttpStatus.CREATED)
    @Transactional
    public Map<String, Object> post3Table() {
        String uid = UUID.randomUUID().toString().substring(0, 8);
        String email = "java_" + uid + "_" + System.nanoTime() + "@example.com";
        Integer customerId = jdbcTemplate.queryForObject(
            "INSERT INTO customer (name, email, phone, city) VALUES (?, ?, ?, ?) RETURNING id",
            Integer.class,
            "Customer_" + uid, email, "555-" + uid, "Benchmark City"
        );
        Integer productId = jdbcTemplate.queryForObject(
            "INSERT INTO product (factory_id, name, category, price, stock) VALUES (1, ?, 'Benchmark Category', 99.99, 100) RETURNING id",
            Integer.class,
            "Product_" + uid
        );
        Long orderId = jdbcTemplate.queryForObject(
            "INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES (?, ?, 1, 99.99, 'COMPLETED') RETURNING id",
            Long.class,
            customerId, productId
        );
        Map<String, Object> res = new HashMap<>();
        res.put("customer_id", customerId);
        res.put("product_id", productId);
        res.put("order_id", orderId);
        return res;
    }

    @PostMapping("/raw/post/4table")
    @ResponseStatus(HttpStatus.CREATED)
    @Transactional
    public Map<String, Object> post4Table() {
        String uid = UUID.randomUUID().toString().substring(0, 8);
        String email = "java_" + uid + "_" + System.nanoTime() + "@example.com";
        Integer factoryId = jdbcTemplate.queryForObject(
            "INSERT INTO factory (name, location, country) VALUES (?, 'Industrial Estate', 'Thailand') RETURNING id",
            Integer.class,
            "Factory_" + uid
        );
        Integer productId = jdbcTemplate.queryForObject(
            "INSERT INTO product (factory_id, name, category, price, stock) VALUES (?, ?, 'Benchmark Category', 99.99, 100) RETURNING id",
            Integer.class,
            factoryId, "Product_" + uid
        );
        Integer customerId = jdbcTemplate.queryForObject(
            "INSERT INTO customer (name, email, phone, city) VALUES (?, ?, ?, ?) RETURNING id",
            Integer.class,
            "Customer_" + uid, email, "555-" + uid, "Benchmark City"
        );
        Long orderId = jdbcTemplate.queryForObject(
            "INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES (?, ?, 1, 99.99, 'COMPLETED') RETURNING id",
            Long.class,
            customerId, productId
        );
        Map<String, Object> res = new HashMap<>();
        res.put("factory_id", factoryId);
        res.put("product_id", productId);
        res.put("customer_id", customerId);
        res.put("order_id", orderId);
        return res;
    }
}
