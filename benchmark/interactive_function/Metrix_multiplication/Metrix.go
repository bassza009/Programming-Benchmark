package main

import "fmt"

func main() {
	const n = 1000
	a := make([]float64, n*n)
	b := make([]float64, n*n)
	res := make([]float64, n*n)

	for i := 0; i < n*n; i++ {
		a[i] = float64(i % n)
		b[i] = float64(i / n)
	}

	fmt.Printf("Starting Matrix Multiplication (Go): %dx%d\n", n, n)

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			var sum float64
			for k := 0; k < n; k++ {
				sum += a[i*n+k] * b[k*n+j]
			}
			res[i*n+j] = sum
		}
	}
	fmt.Printf("Sample Result [0]: %f\n", res[0])
}
