package main

import (
	"fmt"
)

func main() {
	fmt.Println(countPrimes(10000000))
}

func countPrimes(limit int) int {
	count := 0
	for i := 2; i <= limit; i++ {
		isPrime := true
		for j := 2; j*j <= i; j++ {
			if i%j == 0 {
				isPrime = false
				break
			}
		}
		if isPrime {
			count++
		}
	}
	return count
}
