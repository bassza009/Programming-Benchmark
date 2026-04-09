package main

import (
	"fmt"
	"time"
)

func main(){
	start := time.Now()
	for i := 0 ; i <100 ;i++{
		fmt.Println(i)
	}
	
	duration := time.Since(start)
	fmt.Println("Process duration : %v\n",duration)
}