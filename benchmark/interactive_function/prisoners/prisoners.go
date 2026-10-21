package main

import "fmt"

func playOptimal(n int) float64 {
	pardoned := 0
	inDrawer := make([]int, 100)
	for i := 0; i < 100; i++ {
		inDrawer[i] = i
	}

	var seed int64 = 42

	for r := 0; r < n; r++ {
		for i := 99; i > 0; i-- {
			seed = (seed*1664525 + 1013904223) & 0x7fffffff
			j := int(seed % int64(i+1))
			temp := inDrawer[i]
			inDrawer[i] = inDrawer[j]
			inDrawer[j] = temp
		}

		allFound := true
		for prisoner := 0; prisoner < 100; prisoner++ {
			found := false
			reveal := prisoner
			for step := 0; step < 50; step++ {
				card := inDrawer[reveal]
				if card == prisoner {
					found = true
					break
				}
				reveal = card
			}
			if !found {
				allFound = false
				break
			}
		}
		if allFound {
			pardoned++
		}
	}
	return float64(pardoned) / float64(n) * 100.0
}

func main() {
	const n = 1000000
	fmt.Printf("Optimal play wins: %.4f%%\n", playOptimal(n))
}
