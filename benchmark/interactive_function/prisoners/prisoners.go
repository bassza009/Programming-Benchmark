package main

import (
	"fmt"
	"math/rand"
	"time"
)

func playOptimal(n int) float64 {
	pardoned := 0
	inDrawer := make([]int, 100)
	for i := 0; i < 100; i++ {
		inDrawer[i] = i
	}

	for r := 0; r < n; r++ {
		rand.Shuffle(100, func(i, j int) { inDrawer[i], inDrawer[j] = inDrawer[j], inDrawer[i] })

		allFound := true
		for prisoner := 0; prisoner < 100; prisoner++ {
			found := false
			reveal := prisoner
			for go_round := 0; go_round < 50; go_round++ {
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
	return float64(pardoned) / float64(n) * 100
}

func main() {
	rand.Seed(time.Now().UnixNano())
	n := 1000000
	fmt.Printf("Optimal play wins (Go): %.1f%%\n", playOptimal(n))
}
