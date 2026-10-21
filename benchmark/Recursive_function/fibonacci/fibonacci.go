package main

import "fmt"

func fibonacci(n int64) int64 {
	if n <= 1 {
		return n
	}
	return fibonacci(n-1) + fibonacci(n-2)
}

func main() {
	const n int64 = 40
	fmt.Println(fibonacci(n))
}
