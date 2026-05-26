package com.benchmark;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public void run(String... args) throws Exception {
        Long count = entityManager.createQuery("SELECT COUNT(u) FROM User u", Long.class).getSingleResult();
        if (count == 0) {
            insertMockData();
        }
    }

    @Transactional
    public void insertMockData() {
        for (int i = 1; i <= 10000; i++) {
            User user = new User();
            user.setName("User" + i);
            user.setEmail("user" + i + "@example.com");
            entityManager.persist(user);

            Profile profile = new Profile();
            profile.setUser(user);
            profile.setAge(20 + (i % 50));
            profile.setAddress("Address " + i);
            entityManager.persist(profile);

            Order order = new Order();
            order.setUser(user);
            order.setTotalAmount(100.0 + i);
            entityManager.persist(order);

            if (i % 10 == 0) {
                for (int j = 0; j < 5; j++) {
                    OrderItem item = new OrderItem();
                    item.setOrder(order);
                    item.setProductName("Product" + j);
                    item.setPrice(10.0 + j);
                    entityManager.persist(item);
                }
            }

            if (i % 200 == 0) {
                entityManager.flush();
                entityManager.clear();
            }
        }
    }
}
