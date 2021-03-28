import numpy as np


def input_arr(n):
    arr = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        arr[i] = np.array([int(s) for s in input().split()])
    return arr


def print_arr(arr):
    for i in arr.tolist():
        print(' '.join([str(j) for j in i]))


def main():
    n = int(input())
    arr = input_arr(n)
    while True:
        r = int(input())
        if r == 1:
            f = input()
            if f == '+':
                arr += input_arr(n)
            elif f == '-':
                arr -= input_arr(n)
            elif f == '*':
                arr *= input_arr(n)
            elif f == 'dot':
                arr = np.dot(arr, input_arr(n))
        elif r == 2:
            print('Yes' if np.array_equal(arr, np.dot(arr, arr)) else 'No')
        elif r == 3:
            arr = arr.T
        elif r == 4:
            print_arr(arr)
        elif r == 5:
            break


if __name__ == '__main__':
    main()
