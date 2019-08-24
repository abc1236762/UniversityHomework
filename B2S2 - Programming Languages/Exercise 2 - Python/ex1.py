# Written by 410521209 林鈺錦


nums = list(map(float, input("Enter three different numbers: ").split(" ")))

if nums[0] >= nums[1] and nums[0] >= nums[2]:
	print("%.2f is the largest number." % (nums[0]))

if nums[1] >= nums[0] and nums[1] >= nums[2]:
	print("%.2f is the largest number." % (nums[1]))

if nums[2] >= nums[0] and nums[2] >= nums[1]:
	print("%.2f is the largest number." % (nums[2]))
