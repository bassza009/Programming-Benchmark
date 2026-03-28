package main

import (
	"fmt"
)

func main() {
	var door int = 1
	var incrementer = 0

	for current := 1; current <= 100000000; current++ {
		//fmt.Printf("Door %d ", current)

		if current == door {
			fmt.Printf("Door %d Open\n", current)
			incrementer++
			door += 2*incrementer + 1
		} else {
			//fmt.Printf("Closed\n")
		}
	}

}
