package com.benchmark;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
public class BenchmarkController {

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
            return users.stream()
                    .map(u -> {
                        // 💡 เปลี่ยนมาใช้ HashMap แทน Map.of()
                        Map<String, Object> map = new HashMap<>();
                        map.put("id", u.getId());
                        map.put("name", u.getName());
                        map.put("email", u.getEmail());
                        return map;
                    })
                    .collect(Collectors.toList());
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
