FROM python:3.12-slim
WORKDIR /app
# ติดตั้ง Library ที่ต้องใช้
RUN pip install --no-cache-dir psutil
# ก๊อปปี้ไฟล์ทั้งหมดในโปรเจกต์เข้าไปใน Docker
COPY . .
# สั่งรันไฟล์ Benchmark 
CMD ["python3", "door.py"]
