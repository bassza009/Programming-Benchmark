package com.benchmark;

// 💡 ใช้ Java Record: สั้น กระชับ เร็วปรู๊ดปร๊าด และเป็น Immutable ขนานแท้
public record UserDTO(Integer id, String name, String email) {
}
