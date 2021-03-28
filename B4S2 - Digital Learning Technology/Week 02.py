def hw1():
    usd = int(input())
    twd = usd * 30.5
    print(twd)
    print(f'{twd} yuan')
    print(f'{usd} US dollars is {twd} yuan Taiwan dollars')
    print(f'{usd} US dollars={twd} yuan Taiwan dollars')


def hw2():
    c, e, m, p = int(input()), int(input()), int(input()), int(input())
    s = c + e + m + p
    print(s)
    print(s / 4)


def hw3():
    ident = input().upper()
    num = ord(ident[0]) - ord('A') + 1
    print(f'{num:02d}{ident[1:]}')
