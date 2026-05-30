package com.benchmark;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.*;

@RestController
public class BenchmarkController {
    @Autowired
    private UserRepository userRepository;

    @GetMapping("/")
    public Map<String, String> root() {
        return Map.of("status", "success", "message", "Hello Benchmark");
    }

    @GetMapping("/orm/1table")
    public List<UserDTO> ormOneTable() {
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
