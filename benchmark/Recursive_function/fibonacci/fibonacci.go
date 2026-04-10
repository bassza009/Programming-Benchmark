package main

import "fmt"

func fibonacci(n uint64) uint64 {
	if n <= 1 {
		return n
	}
	return fibonacci(n-1) + fibonacci(n-2)
}
func main() {
	fmt.Println(fibonacci(990))
}
