package main

import (
	"fmt"
	"math/rand"
	"time"
)

// โครงสร้างข้อมูลสำหรับเก็บผลลัพธ์
type Result struct {
	Prisoners int
	Strategy  string
	WinRate   float64
	TimeUsed  float64
}

func doTrials(trials, np int, strategy string) Result {
	start := time.Now()
	pardoned := 0

trial:
	for t := 0; t < trials; t++ {
		var drawers [100]int
		for i := 0; i < 100; i++ {
			drawers[i] = i
		}
		rand.Shuffle(100, func(i, j int) {
			drawers[i], drawers[j] = drawers[j], drawers[i]
		})

	prisoner:
		for p := 0; p < np; p++ {
			if strategy == "optimal" {
				prev := p
				for d := 0; d < 50; d++ {
					this := drawers[prev]
					if this == p {
						continue prisoner
					}
					prev = this
				}
			} else {
				var opened [100]bool
				for d := 0; d < 50; d++ {
					var n int
					for {
						n = rand.Intn(100)
						if !opened[n] {
							opened[n] = true
							break
						}
					}
					if drawers[n] == p {
						continue prisoner
					}
				}
			}
			continue trial
		}
		pardoned++
	}

	duration := time.Since(start).Seconds()
	winRate := float64(pardoned) / float64(trials) * 100

	return Result{
		Prisoners: np,
		Strategy:  strategy,
		WinRate:   winRate,
		TimeUsed:  duration,
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())
	const trials = 100000
	var allResults []Result

	// ทำการทดสอบ
	for _, np := range []int{10, 100} {
		for _, strategy := range []string{"random", "optimal"} {
			res := doTrials(trials, np, strategy)
			allResults = append(allResults, res)
		}
	}

	// พิมพ์ตารางผลลัพธ์
	fmt.Printf("\nSimulation count: %d trials\n", trials)
	fmt.Println("----------------------------------------------------------------------")
	fmt.Printf("%-12s | %-12s | %-12s | %-12s\n", "Prisoners", "Strategy", "Win Rate (%)", "Time Used")
	fmt.Println("----------------------------------------------------------------------")
	
	for _, r := range allResults {
		fmt.Printf("%-12d | %-12s | %-12.2f | %-10.4fs\n", 
			r.Prisoners, r.Strategy, r.WinRate, r.TimeUsed)
	}
	fmt.Println("----------------------------------------------------------------------")
}