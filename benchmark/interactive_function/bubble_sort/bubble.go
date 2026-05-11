package main

import (
	"fmt"
)

func main() {
	const n = 20000
	arr := make([]int, n)
	for i := 0; i < n; i++ {
		arr[i] = n - i
	}

	fmt.Printf("Starting Bubble Sort (Go): %d items\n", n)

	for i := 0; i < n; i++ {
		for j := 0; j < n-i-1; j++ {
			if arr[j] > arr[j+1] {
				// Go สามารถสลับค่าได้ในบรรทัดเดียว
				arr[j], arr[j+1] = arr[j+1], arr[j]
			}
		}
	}

	fmt.Printf("Sample Result [0]: %d\n", arr[0])

}
