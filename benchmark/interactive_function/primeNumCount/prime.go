package main

import "fmt"

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

func main() {
	const n = 1000000
	result := countPrimes(n)
	fmt.Printf("Primes count: %d\n", result)
}
