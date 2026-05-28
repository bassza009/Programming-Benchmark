package com.benchmark;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import jakarta.persistence.*;
import java.util.*;
import java.util.stream.Collectors;

@SpringBootApplication
public class Server {
    public static void main(String[] args) {
        SpringApplication.run(Server.class, args);
    }
}

@RestController
class BenchmarkController {

    @PersistenceContext
    private EntityManager entityManager;

    @GetMapping("/")
    public Map<String, String> root() {
        return Map.of("status", "success", "message", "Hello Benchmark");
    }

    @GetMapping("/orm/1table")
    public List<Map<String, Object>> ormOneTable() {
        List<User> users = entityManager.createQuery("SELECT u FROM User u", User.class)
                .setMaxResults(100)
                .getResultList();
        return users.stream().map(u -> {
            Map<String, Object> map = new HashMap<>();
            // 💡 เรียกใช้ตัวแปรตรงๆ และใช้ HashMap เพื่อป้องกัน Error จากค่า Null
            map.put("id", u.id);
            map.put("name", u.name);
            map.put("email", u.email);
            return map;
        }).collect(Collectors.toList());
    }

    @GetMapping("/orm/2join")
    public List<Map<String, Object>> ormTwoJoin() {
        List<Object[]> rows = entityManager.createQuery(
                        "SELECT u.name, p.age FROM User u JOIN u.profile p", Object[].class)
                .setMaxResults(100)
                .getResultList();
        return rows.stream().map(row -> {
            Map<String, Object> map = new HashMap<>();
            map.put("name", row[0]);
            map.put("age", row[1]);
            return map;
        }).collect(Collectors.toList());
    }

    @GetMapping("/orm/3join")
    public List<Map<String, Object>> ormThreeJoin() {
        List<Object[]> rows = entityManager.createQuery(
                        "SELECT u.name, p.age, o.totalAmount FROM User u JOIN u.profile p JOIN u.orders o", Object[].class)
                .setMaxResults(100)
                .getResultList();
        return rows.stream().map(row -> {
            Map<String, Object> map = new HashMap<>();
            map.put("name", row[0]);
            map.put("age", row[1]);
            map.put("total_amount", row[2]);
            return map;
        }).collect(Collectors.toList());
    }

    @GetMapping("/orm/4join")
    public List<Map<String, Object>> ormFourJoin() {
        List<Object[]> rows = entityManager.createQuery(
                        "SELECT u.name, p.age, o.totalAmount, oi.productName FROM OrderItem oi JOIN oi.order o JOIN o.user u JOIN u.profile p", Object[].class)
                .setMaxResults(100)
                .getResultList();
        return rows.stream().map(row -> {
            Map<String, Object> map = new HashMap<>();
            map.put("name", row[0]);
            map.put("age", row[1]);
            map.put("total_amount", row[2]);
            map.put("product_name", row[3]);
            return map;
        }).collect(Collectors.toList());
    }
}

@Entity
@Table(name = "users")
class User {
    @Id public Integer id;
    public String name;
    public String email;

    @OneToOne(mappedBy = "user")
    public Profile profile;

    @OneToMany(mappedBy = "user")
    public List<Order> orders;
}

@Entity
@Table(name = "profiles")
class Profile {
    @Id public Integer id;
    public Integer age;
    public String address;

    @OneToOne
    @JoinColumn(name = "user_id")
    public User user;
}

@Entity
@Table(name = "orders")
class Order {
    @Id public Integer id;
    @Column(name = "total_amount")
    public Double totalAmount;

    @ManyToOne
    @JoinColumn(name = "user_id")
    public User user;

    @OneToMany(mappedBy = "order")
    public List<OrderItem> orderItems;
}

@Entity
@Table(name = "order_items")
class OrderItem {
    @Id public Integer id;
    @Column(name = "product_name")
    public String productName;
    public Double price;

    @ManyToOne
    @JoinColumn(name = "order_id")
    public Order order;
}
