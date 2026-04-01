import time
import math

def main():
    n = 1000

    # 1. เตรียมข้อมูล (ไม่นับรวมในเวลาประมวลผลหลัก)
    # ใช้ list ธรรมดาเพื่อวัดประสิทธิภาพของตัวภาษา Python เอง
    matrix_a = [0.0] * (n * n)
    matrix_b = [0.0] * (n * n)
    result  = [0.0] * (n * n)

    for i in range(n * n):
        matrix_a[i] = float(i % n)
        matrix_b[i] = float(i // n)

    print(f"Starting Matrix Multiplication (Python): {n}x{n}")

 
    for i in range(n):
        for j in range(n):
            sum_val = 0.0
            for k in range(n):
                # สูตรคำนวณ Index สำหรับ Flat Array: (row * n) + k
                sum_val += matrix_a[i * n + k] * matrix_b[k * n + j]
            result[i * n + j] = sum_val



    # 3. แสดงผลลัพธ์ (Output Format เดียวกับภาษาอื่น)


    print(f"Sample Result [0]: {result[0]:.6f}")

if __name__ == "__main__":
    main()