package ucb1

type Step struct {
	arm         int
	totalReward float64
}

func (s Step) Arm() int {
	return s.arm
}

func (s Step) TotalReward() float64 {
	return s.totalReward
}
