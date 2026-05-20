FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

# ก๊อปปี้ไฟล์โค้ดเข้ามา
COPY server.java .

# คอมไพล์โค้ด
RUN javac server.java

# เปิดพอร์ต
EXPOSE 8080

# สั่งรัน
CMD ["java", "server"]