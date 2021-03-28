import numpy as np
import pandas as pd


def hw1():
    n = int(input())
    df = pd.DataFrame()
    for _ in range(n):
        s, m, c, p = [int(s) for s in input().split()]
        row = {'Number': s, 'Math': m, 'Chinese': c, 'Programming': p}
        row['Total'] = m + c + p
        row['Average'] = row['Total'] / 3
        row['Achievement'] = 'pass' if row['Average'] >= 60 else 'fail'
        df = df.append(row, ignore_index=True)
    df['Number'] = df['Number'].astype(int)
    df['Math'] = df['Math'].astype(int)
    df['Chinese'] = df['Chinese'].astype(int)
    df['Programming'] = df['Programming'].astype(int)
    df['Total'] = df['Total'].astype(int)
    df = df[['Number', 'Math', 'Chinese', 'Programming',
             'Total', 'Average', 'Achievement']]
    df.to_html('result.html')


def hw2():
    def input_arr() -> np.ndarray:
        n, m = [int(s) for s in input().split()]
        arr = np.zeros((n, m), dtype=np.int64)
        for i in range(n):
            arr[i] = np.array([int(s) for s in input().split()])
        return arr
    arr = input_arr()
    while True:
        if (r := int(input('request: '))) == 1:
            n, m = [int(s) for s in input().split()]
            arr = arr.reshape((n, m))
        elif r == 2:
            try:
                arr = np.dot(arr, input_arr())
            except ValueError:
                print('fail')
        elif r == 3:
            arr = arr.T
        elif r == 4:
            print(arr)
        else:
            break
