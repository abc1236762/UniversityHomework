from os import path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 資料網址
DATA_URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data'
# 資料標籤
DATA_LABEL = ['sex', 'length', 'diameter', 'height', 'whole weight',
              'shucked weight', 'viscera weight', 'shell weight', 'rings']


# 取得資料
def get_data() -> (np.ndarray, np.ndarray):
    if not path.exists('data.csv'):
        # 如果在本地沒有資料，先從網址上抓
        df = pd.read_csv(DATA_URL)
        # 因為來源沒有欄位標籤，要設置
        df.columns = DATA_LABEL
        # 儲存成csv
        df.to_csv('data.csv', index=False)
    else:
        # 讀取資料
        df = pd.read_csv('data.csv')
    # 3種不同的weight為x，DATA_LABEL[5]至DATA_LABEL[7]對應3種不同的weight標籤
    x = np.array(df[DATA_LABEL[5:8]])
    # whole weight為y，DATA_LABEL[4]對應whole weight的標籤
    y = np.array(df[DATA_LABEL[4]])
    return x, y


# 設定圖表的各種屬性
def config_plt(title: str, xlabel: str, ylabel: str):
    # 設定圖表的尺寸、標題、x軸標籤、y軸標籤、緊的輸出、有格線
    plt.figure(figsize=(12.0, 6.75))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.grid(True)


# 產生資料的圖表
def gen_data_polt(x: np.ndarray, y: np.ndarray):
    # 取得標題
    title = ','.join(
        [s.split()[0] for s in DATA_LABEL[5:8]]) + ' - ' + DATA_LABEL[4]
    # 設定圖表
    config_plt(title, DATA_LABEL[4].split()[1], DATA_LABEL[4])
    # 針對3種不同的weight，分別以3種不同的顏色繪製與whole weight對應的關係
    for i, c in enumerate(['r', 'g', 'b']):
        # 因為3種不同weight的標籤在DATA_LABEL[5]開始，因此DATA_LABEL[5+i]
        plt.scatter(x[..., i], y, color=c, label=DATA_LABEL[5+i])
    # 繪製不同顏色代表的標記
    plt.legend(loc='lower right')
    # 儲存圖表
    plt.savefig(f'{title}.png')


# 產生預測與答案的圖表
def gen_result_polt(y_pred: np.ndarray, y: np.ndarray, note: str):
    # 取得標題
    title = f'prediction - answer results ({note})'
    # 設定圖表
    config_plt(title, 'prediction', 'answer')
    # 繪製預測與答案的關係
    plt.scatter(y_pred, y, color='black')
    # 儲存圖表
    plt.savefig(f'{title}.png')


# 主程式
def main():
    # 先取得資料並產生圖表
    x, y = get_data()
    gen_data_polt(x, y)
    # 將資料切成訓練和測試用
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=10, random_state=0x749487)
    # 建立一個套用至訓練資料集的線性複回歸模型，因為x不是1D的所以是線性複回歸
    lr = LinearRegression().fit(x_train, y_train)
    # 用訓練資料集進行預測得到訓練資料集的預設結果，與其答案進行比較並產生圖表
    y_train_pred = lr.predict(x_train)
    gen_result_polt(y_train_pred, y_train, 'train')
    # 用測試資料集進行預測得到測試資料集的預設結果，與其答案進行比較並產生圖表
    y_test_pred = lr.predict(x_test)
    gen_result_polt(y_test_pred, y_test, 'test')
    # 輸出測試資料集、其答案以及預測結果
    print(f'x_test\n{x_test}')
    print(f'y_test\n{y_test}')
    print(f'y_test_pred\n{y_test_pred}')


if __name__ == '__main__':
    # 進入主程式
    main()
