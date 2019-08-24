package ucb1

import (
	`math`
	`math/rand`
	`time`
)

func init() {
	rand.Seed(time.Now().UnixNano())
}

type UCB1 struct {
	probabilities []float64
	cost          float64
	rewardsPerArm []float64
	timesPerArm   []int
	steps         []Step
	totalTimes    int
	totalReward   float64
}

func New(probabilities []float64, cost float64) *UCB1 {
	var rewardsPerArm = make([]float64, len(probabilities))
	var steps = make([]Step, 0)
	var timesPerArm = make([]int, len(probabilities))
	return &UCB1{
		probabilities: probabilities,
		cost:          cost,
		rewardsPerArm: rewardsPerArm,
		timesPerArm:   timesPerArm,
		steps:         steps,
	}
}

func (u *UCB1) upperBound(arm int) float64 {
	return math.Sqrt(2 * math.Log(float64(u.totalTimes)) /
		float64(u.timesPerArm[arm]))
}

func (u *UCB1) avgReward(arm int) float64 {
	return u.rewardsPerArm[arm] / float64(u.timesPerArm[arm])
}

func (u *UCB1) getReward(arm int) (reward float64) {
	reward = -u.cost
	if randVal := rand.Float64(); u.probabilities[arm] >= randVal {
		reward += 1.0
	}
	return
}

func (u *UCB1) GuessArm() (selectedArm int) {
	if u.totalTimes < len(u.probabilities) {
		selectedArm = u.totalTimes
	} else {
		var maxUCB float64
		for arm := range u.probabilities {
			if ucb := u.avgReward(arm) + u.upperBound(arm); ucb > maxUCB {
				selectedArm = arm
				maxUCB = ucb
			}
		}
	}
	
	var reward = u.getReward(selectedArm)
	u.rewardsPerArm[selectedArm] += reward
	u.totalReward += reward
	u.steps = append(u.steps, Step{selectedArm, u.totalReward})
	u.totalTimes += 1
	u.timesPerArm[selectedArm] += 1
	return
}

func (u *UCB1) Probabilities() []float64 {
	return u.probabilities
}

func (u *UCB1) Cost() float64 {
	return u.cost
}

func (u *UCB1) RewardsPerArm() []float64 {
	return u.rewardsPerArm
}

func (u *UCB1) TimesPerArm() []int {
	return u.timesPerArm
}

func (u *UCB1) Steps() []Step {
	return u.steps
}

func (u *UCB1) TotalTimes() int {
	return u.totalTimes
}

func (u *UCB1) TotalReward() float64 {
	return u.totalReward
}
