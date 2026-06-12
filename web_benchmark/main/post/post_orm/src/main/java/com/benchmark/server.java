package com.benchmark;

import jakarta.persistence.*;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@SpringBootApplication
public class server {
    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(server.class);
        
        // ตั้งค่า Database และ Port ภายในไฟล์เดียวจบ (ไม่ต้องใช้ application.properties)
        app.setDefaultProperties(Map.of(
                "server.port", "8005",
                "spring.datasource.url", "jdbc:mysql://127.0.0.1:3306/benchmark_db",
                "spring.datasource.username", "admin",
                "spring.datasource.password", "secret",
                "spring.datasource.driver-class-name", "com.mysql.cj.jdbc.Driver",
                "spring.jpa.hibernate.ddl-auto", "none"
        ));
        
        app.run(args);
    }
}

// --- Entities ---
@Entity @Table(name = "users")
class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) public Long id;
    public String name;
    public String email;
}

@Entity @Table(name = "profiles")
class Profile {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) public Long id;
    public Long userId;
    public String bio;
    public String phone;
}

@Entity @Table(name = "orders")
class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) public Long id;
    public Long userId;
    public BigDecimal totalAmount;
}

@Entity @Table(name = "order_items")
class OrderItem {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) public Long id;
    public Long orderId;
    public String productName;
    public BigDecimal price;
}

// --- Repositories ---
interface UserRepository extends JpaRepository<User, Long> {}
    }
interface ProfileRepository extends JpaRepository<Profile, Long> {}
interface OrderRepository extends JpaRepository<Order, Long> {}
interface OrderItemRepository extends JpaRepository<OrderItem, Long> {}

// --- Controller ---
@RestController
class BenchmarkController {
    private final UserRepository userRepo;
    private final ProfileRepository profileRepo;
    private final OrderRepository orderRepo;
    private final OrderItemRepository orderItemRepo;

    public BenchmarkController(UserRepository u, ProfileRepository p, OrderRepository o, OrderItemRepository oi) {
        this.userRepo = u; this.profileRepo = p; this.orderRepo = o; this.orderItemRepo = oi;
    }

    private String getHex() {
        return UUID.randomUUID().toString().substring(0, 8);
    }

    @PostMapping("/orm/post/1table")
    @Transactional
    public ResponseEntity<?> post1Table() {
        String randId = getHex();
        User user = new User();
        user.name = "User_" + randId;
        user.email = "test_" + randId + "@example.com";
        user = userRepo.save(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("user_id", user.id));
    }

    @PostMapping("/orm/post/2table")
    @Transactional
    public ResponseEntity<?> post2Table() {
        String randId = getHex();
        User user = new User();
        user.name = "User_" + randId; user.email = "test_" + randId + "@example.com";
        user = userRepo.save(user);

        Profile profile = new Profile();
        profile.userId = user.id; profile.bio = "Bio for user " + user.id; profile.phone = "555-" + randId;
        profileRepo.save(profile);

        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("user_id", user.id));
    }

    @PostMapping("/orm/post/3table")
    @Transactional
    public ResponseEntity<?> post3Table() {
        String randId = getHex();
        User user = new User();
        user.name = "User_" + randId; user.email = "test_" + randId + "@example.com";
        user = userRepo.save(user);

        Profile profile = new Profile();
        profile.userId = user.id; profile.bio = "Bio for user " + user.id; profile.phone = "555-" + randId;
        profileRepo.save(profile);

        Order order = new Order();
        order.userId = user.id; order.totalAmount = new BigDecimal("100.00");
        orderRepo.save(order);

        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("user_id", user.id));
    }

    @PostMapping("/orm/post/4table")
    @Transactional
    public ResponseEntity<?> post4Table() {
        String randId = getHex();
        User user = new User();
        user.name = "User_" + randId; user.email = "test_" + randId + "@example.com";
        user = userRepo.save(user);

        Profile profile = new Profile();
        profile.userId = user.id; profile.bio = "Bio for user " + user.id; profile.phone = "555-" + randId;
        profileRepo.save(profile);

        Order order = new Order();
        order.userId = user.id; order.totalAmount = new BigDecimal("100.00");
        order = orderRepo.save(order);

        OrderItem i1 = new OrderItem(); i1.orderId = order.id; i1.productName = "Product_" + randId + "_1"; i1.price = new BigDecimal("25.00");
        OrderItem i2 = new OrderItem(); i2.orderId = order.id; i2.productName = "Product_" + randId + "_2"; i2.price = new BigDecimal("75.00");
        orderItemRepo.saveAll(List.of(i1, i2));

        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("user_id", user.id));
    }
}