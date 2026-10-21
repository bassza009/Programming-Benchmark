package main

import "fmt"

func main() {
	const n = 10000
	arr := make([]int, n)
	for i := 0; i < n; i++ {
		arr[i] = n - i
	}

	for i := 0; i < n; i++ {
		for j := 0; j < n-i-1; j++ {
			if arr[j] > arr[j+1] {
				temp := arr[j]
				arr[j] = arr[j+1]
				arr[j+1] = temp
			}
		}
	}

	fmt.Printf("Sample Result [0]: %d, [%d]: %d\n", arr[0], n-1, arr[n-1])
}
