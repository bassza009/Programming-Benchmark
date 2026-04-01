package main

import (
	"fmt"
)

// ใช้ Struct เพื่อเก็บข้อมูล Matrix แบบ 1 มิติ (Flat Array)
// ซึ่งจะช่วยเรื่อง Performance และ Memory Locality ในงานวิจัยได้ดีกว่า
type matrix struct {
	rows int
	cols int
	data []float64
}

func newMatrix(rows, cols int) *matrix {
	return &matrix{
		rows: rows,
		cols: cols,
		data: make([]float64, rows*cols),
	}
}

func (m1 *matrix) multiply(m2 *matrix) (*matrix, bool) {
	// เช็คเงื่อนไขการคูณ Matrix: หลักของตัวหน้าต้องเท่ากับแถวของตัวหลัง
	if m1.cols != m2.rows {
		return nil, false
	}

	result := newMatrix(m1.rows, m2.cols)

	// Triple Nested Loop (ลูป 3 ชั้น) ตามมาตรฐานงานวิจัย CPU-bound
	for i := 0; i < m1.rows; i++ {
		for j := 0; j < m2.cols; j++ {
			var sum float64
			for k := 0; k < m1.cols; k++ {
				// คำนวณตำแหน่ง Index ใน Flat Array: (row * total_cols) + col
				sum += m1.data[i*m1.cols+k] * m2.data[k*m2.cols+j]
			}
			result.data[i*result.cols+j] = sum
		}
	}
	return result, true
}

func main() {
	const n = 1000 // ขนาด 1000x1000 ตามที่คุณต้องการทดสอบ

	// 1. เตรียมข้อมูล
	a := newMatrix(n, n)
	b := newMatrix(n, n)

	for i := 0; i < n*n; i++ {
		a.data[i] = float64(i % n)
		b.data[i] = float64(i / n)
	}

	// 2. เริ่มการประมวลผลและจับเวลา
	fmt.Printf("Starting Matrix Multiplication: %d x %d\n", n, n)

	p, ok := a.multiply(b)

	if !ok {
		fmt.Println("Error: Matrices are not conformable for multiplication")
		return
	}

	fmt.Printf("Sample Result [0]: %f\n", p.data[0])
}
