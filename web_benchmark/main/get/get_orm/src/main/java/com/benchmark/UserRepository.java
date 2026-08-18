package com.benchmark;
import java.util.List;
import java.util.Map;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {
    
    //  ใช้ DTO ในการรับข้อมูลเพื่อความเร็วสูงสุดและกัน JSON วนลูป
    @Query(value = "SELECT id, name, email FROM users LIMIT 100", nativeQuery = true)
    List<Map<String, Object>> get1Table();

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
