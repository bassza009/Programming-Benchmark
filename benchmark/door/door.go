package main

import (
	"fmt"
	"time"
)

func main() {
    var door int = 1
    var incrementer = 0
	start := time.Now()
    for current := 1; current <= 10000; current++ {
        fmt.Printf("Door %d ", current)

        if current == door {
            fmt.Printf("Open\n")
            incrementer++
            door += 2*incrementer + 1
        } else {
            fmt.Printf("Closed\n")
        }
    }
	duration := time.Since(start)

	fmt.Println("Task process : ",duration)
}
