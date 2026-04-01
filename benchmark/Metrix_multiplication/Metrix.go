package main

import "fmt"

func main() {
	const n = 1000

	metrix_a := make([][]float64, n)
	metrix_b := make([][]float64, n)
	results := make([][]float64, n)
	for i := 0; i < n; i++ {
		metrix_a[i] = make([]float64, n)
		metrix_b[i] = make([]float64, n)
		results[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			metrix_a[i][j] = float64(i + j)
			metrix_b[i][j] = float64(i + j)
		}
	}

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			var sum float64
			for k := 0; k < n; k++ {
				sum += metrix_a[i][k] * metrix_b[j][k]

			}
			results[i][j] = sum

		}
	}
	fmt.Println("Result[0][0] : ", results[0][0])
}
