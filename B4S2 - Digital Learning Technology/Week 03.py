def hw1():
    c, e, m, p = int(input()), int(input()), int(input()), int(input())
    avg = (c + e + m + p) / 4
    print(avg)
    if 80 <= avg:
        print('A')
    elif 70 <= avg < 80:
        print('B')
    elif 60 <= avg < 70:
        print('C')
    else:
        print('D')
    print('pass' if avg >= 60 else 'not pass')


def hw2():
    while True:
        n, s = int(input()), 0
        if n == 0:
            break
        for i in range(1, n + 1):
            s += i ** i
        print(s % 10)


def hw3():
    while True:
        n = int(input())
        if n == 0:
            break
        arr, cnt = [0] * n, 0
        for i in range(n):
            arr[i] = int(input())
        for i in range(n):
            for j in range(i + 1, n):
                if arr[i] > arr[j]:
                    cnt += 1
        print(cnt)
