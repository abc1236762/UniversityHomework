# Written by 410521209 林鈺錦


def add_nums(a, b):
	return a + b


def main():
	nums = list(map(int, input("Enter two numbers: ").split(" ")))
	print("sum = " + str(add_nums(nums[0], nums[1])))


if __name__ == "__main__":
	main()
