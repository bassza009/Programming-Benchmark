package main

import "fmt"

func factorial(n int) float64 {
	if n <= 1 {
		return 1.0
	}
	return float64(n) * factorial(n-1)
}

func main() {
	const n = 100
	fmt.Printf("%.6e\n", factorial(n))
}
