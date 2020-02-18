import datetime
import glob
import itertools
import json
import os
import re
from typing import Dict

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import KFold, cross_validate
from sklearn.tree import DecisionTreeClassifier, export_text

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(8, 8))

OD = 'cwbopendata'
DS = 'dataset'
LC = 'location'
LN = 'locationName'
WE = 'weatherElement'
TM = 'time'
EN = 'elementName'
OT = 'obsTime'
EV = 'elementValue'
VL = 'value'

reg_of_loc = {
    '板橋': '北部', '淡水': '北部', '鞍部': '北部', '臺北': '北部', '竹子湖': '北部',
    '基隆': '北部', '彭佳嶼': '北部', '新屋': '北部', '新竹': '北部', '嘉義': '中部',
    '臺中': '中部', '阿里山': '中部', '玉山': '中部', '日月潭': '中部', '梧棲': '中部',
    '臺南': '南部', '高雄': '南部', '恆春': '南部', '花蓮': '東部', '蘇澳': '東部',
    '宜蘭': '東部', '大武': '東部', '成功': '東部', '蘭嶼': '東部', '臺東': '東部',
    '金門': '外島', '東吉島': '外島', '澎湖': '外島', '馬祖': '外島',
}
index_labels_of_data_type = {'每日統計': '日期', '逐時觀測': '時間'}


def parse_datetime(datetime_str: str):
    date_str, time_str = datetime_str.split()
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    if time_str == '24:00':
        time_str = '00:00'
        date += datetime.timedelta(days=1)
    time = datetime.datetime.strptime(time_str, '%H:%M')
    return date + datetime.timedelta(hours=time.hour, minutes=time.minute)


def preprocess_json():
    orig_data = json.load(open('C-B0024-002.json'))[OD][DS][LC]
    loc_n = len(orig_data)
    weathers = {}
    for data_type_i in range(2):
        for loc_i in range(loc_n):
            loc_data = orig_data[loc_i]
            loc = loc_data[LN].split(',')[1]
            data_type = loc_data[WE][data_type_i][EN]
            weather = {}
            for d in loc_data[WE][data_type_i][TM]:
                if data_type_i == 0:
                    dt = parse_datetime(d[OT])
                elif data_type_i == 1:
                    dt = datetime.datetime.strptime(d[OT], '%Y-%m-%d')
                if '測站' not in weather:
                    weather['測站'] = {}
                weather['測站'][dt] = loc_data[LN].split(',')[1]
                for e in d[WE]:
                    name, value = e[EN], e[EV][VL]
                    if name not in weather:
                        weather[name] = {}
                    if name == '風向':
                        value = value.split(',')[0]
                    if name == '降水量' and value == 'T':
                        value = '0.05'
                    try:
                        value = float(value)
                        if value < 0:
                            value = ''
                    except:
                        pass
                    weather[name][dt] = value
            kind = f'{data_type}_{reg_of_loc[loc]}'
            if kind not in weathers:
                weathers[kind] = pd.DataFrame()
            weathers[kind] = pd.concat([weathers[kind], pd.DataFrame(weather)])
    os.mkdir('data')
    for kind, weather in weathers.items():
        index_label = index_labels_of_data_type[kind[:kind.index('_')]]
        weather.to_csv(os.path.join('data', kind+'.csv'),
                       index_label=index_label)


def analysis_hourly_data(dfs_with_reg: Dict[str, pd.DataFrame]):
    needed_col_labels = ['測站氣壓', '溫度', '相對濕度', '風速', '降水量']

    dir_path = f'plot/逐時觀測'
    os.makedirs(dir_path, exist_ok=True)
    for x_label, y_label in itertools.combinations(needed_col_labels, r=2):
        plt.clf()
        x_min = min([df[x_label].min() for df in dfs_with_reg.values()])
        x_max = max([df[x_label].max() for df in dfs_with_reg.values()])
        y_min = min([df[y_label].min() for df in dfs_with_reg.values()])
        y_max = max([df[y_label].max() for df in dfs_with_reg.values()])
        for reg, df in dfs_with_reg.items():
            x, y = df[x_label], df[y_label]
            plt.scatter(x, y, s=5, alpha=0.6, edgecolors='none', label=reg)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
        plt.legend(loc=2)
        plt.axis([x_min, x_max, y_min, y_max])
        plt.savefig(os.path.join(f'{dir_path}/{x_label}_{y_label}.png'),
                    bbox_inches='tight')


def get_rainfall_class(x: float) -> int:
    if x == 0:
        return 0
    if 0 < x <= 0.4:  # 微雨
        return 1
    elif 0.4 < x <= 1.0:  # 小雨
        return 2
    elif 1.0 < x <= 2.5:  # 中雨
        return 3
    elif 2.5 < x <= 8.0:  # 大雨
        return 4
    elif 8.0 < x <= 15.0:  # 豪雨
        return 5
    elif 15.0 < x <= 21.0:  # 大豪雨
        return 6
    elif 21.0 < x:  # 超大豪雨
        return 7
    return -1


def make_classify_data(dfs_with_reg: Dict[str, pd.DataFrame]):
    x, y = [], []
    needed_col_labels = ['溫度', '相對濕度', '風速']
    for _, dfs in dfs_with_reg.items():
        dfs = dfs.sample(frac=1)
        for _, row in dfs.iterrows():
            yi = get_rainfall_class(row['降水量'])
            if yi >= 0:
                x.append(row[needed_col_labels])
                y.append(yi)
    x, y = np.array(x, dtype=np.float64), np.array(y, dtype=np.int32)
    os.mkdir('classify')
    np.save('classify/x.npy', x)
    np.save('classify/y.npy', y)


def classify_reg(dfs_with_reg: Dict[str, pd.DataFrame]):
    if not os.path.exists('classify'):
        make_classify_data(dfs_with_reg)
    x, y = np.load('classify/x.npy'), np.load('classify/y.npy')
    x = np.nan_to_num(x)
    x = PCA(n_components=1).fit_transform(x)
    dtc = DecisionTreeClassifier()
    p = 0
    plt.figure(figsize=(15, 10))
    plt.clf()
    for train_is, test_is in KFold(n_splits=6, shuffle=True).split(x):
        p += 1
        x_train, x_test = x[train_is], x[test_is]
        y_train, y_test = y[train_is], y[test_is]
        dtc.fit(x_train, y_train)
        y_pred = dtc.predict(x_test)
        score = dtc.score(x_test, y_test)
        plt.subplot(2, 3, p)
        plt.scatter(x_train, y_train, s=2, label='訓練')
        plt.scatter(x_test, y_test, s=2, label='測試')
        plt.scatter(x_test, y_pred, s=2, label='預測')
        plt.xlabel('使用PCA降至一維之數據')
        plt.ylabel('降雨量等級')
        plt.title(f'K-Fold {p}/6：準確率{score*100:.4f}%')
        plt.legend()
    plt.savefig(os.path.join(f'classify.png'), bbox_inches='tight')


if __name__ == '__main__':
    if not os.path.exists('data'):
        preprocess_json()
    pattern = re.compile(r'^data[/\\](\S{4})_(\S{2})\.csv$')
    daily_dfs_with_reg = {}
    hourly_dfs_with_reg = {}
    for filepath in glob.glob(os.path.normpath('data/*.csv')):
        data_type, reg_of_loc = pattern.findall(filepath)[0]
        df = pd.read_csv(filepath)
        if data_type == '逐時觀測':
            hourly_dfs_with_reg[reg_of_loc] = df
    analysis_hourly_data(hourly_dfs_with_reg)
    classify_reg(hourly_dfs_with_reg)
