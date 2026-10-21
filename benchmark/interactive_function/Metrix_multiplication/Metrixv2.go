package main

import "fmt"

func main() {
	const n = 1000
	a := make([]float64, n*n)
	b := make([]float64, n*n)
	result := make([]float64, n*n)

	for i := 0; i < n*n; i++ {
		a[i] = float64(i % n)
		b[i] = float64(i / n)
	}

	for i := 0; i < n; i++ {
		rowOffset := i * n
		for j := 0; j < n; j++ {
			var sum float64 = 0.0
			for k := 0; k < n; k++ {
				sum += a[rowOffset+k] * b[k*n+j]
			}
			result[rowOffset+j] = sum
		}
	}

	fmt.Printf("Sample Result [0]: %.2f\n", result[0])
}
