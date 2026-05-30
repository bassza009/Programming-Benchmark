package com.benchmark;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.*;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {
    
    // 💡 ใช้ DTO ในการรับข้อมูลเพื่อความเร็วสูงสุดและกัน JSON วนลูป
    @Query("SELECT new com.benchmark.UserDTO(u.id, u.name, u.email) FROM User u")
    List<UserDTO> get1Table(org.springframework.data.domain.Pageable pageable);

    default List<UserDTO> get1Table() {
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
