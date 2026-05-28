package com.benchmark;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import jakarta.persistence.*;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.*;

@SpringBootApplication
public class Server {
    public static void main(String[] args) {
        SpringApplication.run(Server.class, args);
    }
}

@RestController
class BenchmarkController {

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/")
    public Map<String, String> root() {
        return Map.of("status", "success", "message", "Hello Benchmark");
    }

    @GetMapping("/orm/1table")
    public List<Map<String, Object>> ormOneTable() {
        return userRepository.get1Table();
    }

    @GetMapping("/orm/2join")
    public List<Map<String, Object>> ormTwoJoin() {
        return userRepository.get2Join();
    }

    @GetMapping("/orm/3join")
    public List<Map<String, Object>> ormThreeJoin() {
        return userRepository.get3Join();
    }

    @GetMapping("/orm/4join")
    public List<Map<String, Object>> ormFourJoin() {
        return userRepository.get4Join();
    }
}

// ---------------- Entities ---------------- //

@Entity
@Table(name = "users")
class User {
    @Id public Integer id;
    public String name;
    public String email;
    @OneToOne(mappedBy = "user") public Profile profile;
    @OneToMany(mappedBy = "user") public List<Order> orders;
}

@Entity
@Table(name = "profiles")
class Profile {
    @Id public Integer id;
    public Integer age;
    public String address;
    @OneToOne @JoinColumn(name = "user_id") public User user;
}

@Entity
@Table(name = "orders")
class Order {
    @Id public Integer id;
    @Column(name = "total_amount") public Double totalAmount;
    @ManyToOne @JoinColumn(name = "user_id") public User user;
    @OneToMany(mappedBy = "order") public List<OrderItem> orderItems;
}

@Entity
@Table(name = "order_items")
class OrderItem {
    @Id public Integer id;
    @Column(name = "product_name") public String productName;
    public Double price;
    @ManyToOne @JoinColumn(name = "order_id") public Order order;
}

// ---------------- Repository (The Magic Happens Here) ---------------- //

@Repository
interface UserRepository extends JpaRepository<User, Integer> {
    
    // 💡 ใช้ "new map(...)" ตัดปัญหาทุกอย่าง ดึงเฉพาะคอลัมน์ที่ต้องการ
    @Query(value = "SELECT new map(u.id as id, u.name as name, u.email as email) FROM User u")
    List<Map<String, Object>> get1Table(org.springframework.data.domain.Pageable pageable);

    default List<Map<String, Object>> get1Table() {
        return get1Table(org.springframework.data.domain.PageRequest.of(0, 100));
    }

    @Query(value = "SELECT new map(u.name as name, p.age as age) FROM User u JOIN u.profile p")
    List<Map<String, Object>> get2Join(org.springframework.data.domain.Pageable pageable);

    default List<Map<String, Object>> get2Join() {
        return get2Join(org.springframework.data.domain.PageRequest.of(0, 100));
    }

    @Query(value = "SELECT new map(u.name as name, p.age as age, o.totalAmount as total_amount) FROM User u JOIN u.profile p JOIN u.orders o")
    List<Map<String, Object>> get3Join(org.springframework.data.domain.Pageable pageable);

    default List<Map<String, Object>> get3Join() {
        return get3Join(org.springframework.data.domain.PageRequest.of(0, 100));
    }

    @Query(value = "SELECT new map(u.name as name, p.age as age, o.totalAmount as total_amount, oi.productName as product_name) FROM User u JOIN u.profile p JOIN u.orders o JOIN o.orderItems oi")
    List<Map<String, Object>> get4Join(org.springframework.data.domain.Pageable pageable);

    default List<Map<String, Object>> get4Join() {
        return get4Join(org.springframework.data.domain.PageRequest.of(0, 100));
    }
}