package main

import "fmt"

func main() {
	const n = 1000000
	doors := make([]bool, n+1)

	for pass := 1; pass <= n; pass++ {
		for d := pass; d <= n; d += pass {
			doors[d] = !doors[d]
		}
	}

	openCount := 0
	for i := 1; i <= n; i++ {
		if doors[i] {
			openCount++
		}
	}
	fmt.Printf("Open doors: %d\n", openCount)
}
