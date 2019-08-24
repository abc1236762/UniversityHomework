package main

import (
	`fmt`
	
	`./ucb1`
)

func main() {
	var times = 2000
	var timesNeedRepo = []int{10, 50, 100, 500, 1000, 2000}
	var probabilities = []float64{0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70}
	var cost = 0.7
	
	var ucb = ucb1.New(probabilities, cost)
	for i := 0; i < times; i++ {
		ucb.GuessArm()
	}
	
	for _, time := range timesNeedRepo {
		var armStr string
		if time == ucb.TotalTimes() {
			armStr = "×"
		} else {
			armStr = fmt.Sprintf("%d", ucb.Steps()[time].Arm()+1)
		}
		fmt.Printf("time %-4d: total reward %7.2f, next arm %s\n", time,
			ucb.Steps()[time-1].TotalReward(), armStr)
	}
}
