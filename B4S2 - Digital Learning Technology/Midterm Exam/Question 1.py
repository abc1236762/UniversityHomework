def input_x():
    x = ''
    while True:
        x = input()
        if x == 'end':
            return 0
        if x in ['GBP', 'KRW', 'NTD', 'USD', 'EUR', 'JPY']:
            return x
        print("ERROR!!Input again!!")


def input_n():
    n = 0
    while True:
        n = int(input())
        if n >= 0:
            return n
        print("N cannot smaller than 0!!Input again!!")


def input_y():
    y = ''
    while True:
        y = input()
        if y in ['GBP', 'KRW', 'NTD', 'USD', 'EUR', 'JPY']:
            return y
        print("ERROR!!Input again!!")


def change(x, y, n):
    dt = {'GBP': 1, 'NTD': 37.7412, 'KRW': 1526.73, 'USD': 1.2588, 'JPY': 134.99}
    return n / dt[x] * dt[y]


def main():
    while True:
        x = input_x()
        if x == 0:
            break
        n = input_n()
        y = input_y()
        c = change(x, y, n)
        print(f'{n} {x} = {c:.3f} {y}')


if __name__ == '__main__':
    main()
