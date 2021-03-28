'''
$ conda activate ppa && conda list
# packages in environment at /home/user/miniconda3/envs/ppa:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main
astroid                   2.4.1                    py38_0
autopep8                  1.4.4                      py_0
blas                      1.0                         mkl
ca-certificates           2020.1.1                      0
certifi                   2020.4.5.1               py38_0
intel-openmp              2020.1                      217
isort                     4.3.21                   py38_0
joblib                    0.15.1                     py_0
lazy-object-proxy         1.4.3            py38h7b6447c_0
ld_impl_linux-64          2.33.1               h53a641e_7
libedit                   3.1.20181209         hc058e9b_0
libffi                    3.3                  he6710b0_1
libgcc-ng                 9.1.0                hdf63c60_0
libgfortran-ng            7.3.0                hdf63c60_0
libstdcxx-ng              9.1.0                hdf63c60_0
mccabe                    0.6.1                    py38_1
mkl                       2020.1                      217
mkl-service               2.3.0            py38he904b0f_0
mkl_fft                   1.0.15           py38ha843d7b_0
mkl_random                1.1.1            py38h0573a6f_0
ncurses                   6.2                  he6710b0_1
numpy                     1.18.1           py38h4f9e942_0
numpy-base                1.18.1           py38hde5b4d6_1
openssl                   1.1.1g               h7b6447c_0
pip                       20.0.2                   py38_3
pycodestyle               2.6.0                      py_0
pylint                    2.5.2                    py38_0
python                    3.8.3                hcff3b4d_0
readline                  8.0                  h7b6447c_0
rope                      0.17.0                     py_0
scikit-learn              0.22.1           py38hd81dba3_0
scipy                     1.4.1            py38h0b6359f_0
setuptools                47.1.1                   py38_0
six                       1.15.0                     py_0
sqlite                    3.31.1               h62c20be_1
tk                        8.6.8                hbc83047_0
toml                      0.10.0             pyh91ea838_0
wheel                     0.34.2                   py38_0
wrapt                     1.11.2           py38h7b6447c_0
xz                        5.2.5                h7b6447c_0
zlib                      1.2.11               h7b6447c_3
'''

import json
import socketserver
from datetime import datetime, timedelta
from http import HTTPStatus, server
from multiprocessing.pool import ThreadPool
from os import path
from typing import Dict, List, Optional, Union
from urllib.parse import parse_qs, unquote, urlparse
from urllib.request import urlopen

import numpy as np
from sklearn.svm import SVR

__all__ = ['PORT', 'run_server']

PORT = 9487 # 會在哪一埠執行網站


class Handler(server.SimpleHTTPRequestHandler):
    '''處理HTTP請求的類別'''

    # 資料API的網址
    _data_url = 'https://data.coa.gov.tw/Service/OpenData/FromM/{}.aspx'

    # 資料來源的相關資料，網址的名稱部分對應需要的各項欄位以及對應顯示名稱
    _data_sources = {
        'PoultryTransBoiledChickenData': {
            '白肉雞(2.0Kg以上)': '白肉雞（2.0kg以上）',
            '白肉雞(1.75-1.95Kg)': '白肉雞（1.75~1.95kg）',
            '白肉雞(門市價高屏)': '白肉雞（門市價，高屏）',
            '雞蛋(產地)': '雞蛋（產地）',
        },
        'PoultryTransLocalChickenData': {
            '黑羽土雞公舍飼': '黑羽土雞（南區，公，舍飼）',
            '黑羽土雞母舍飼': '黑羽土雞（南區，母，舍飼）',
        },
        'PoultryTransGooseDuckData': {
            '肉鵝(白羅曼)': '肉鵝（白羅曼）',
            '正番鴨(公)': '正番鴨（公）',
            '土番鴨(75天)': '土番鴨（75天）',
            '鴨蛋(新蛋)(台南)': '鴨蛋（新蛋，台南）',
        },
        'PoultryTransLocalRedChickenData': {
            '紅羽土雞北區': '紅羽土雞（北區）',
            '紅羽土雞中區': '紅羽土雞（中區）',
            '紅羽土雞南區': '紅羽土雞（南區）',
        },
        'PoultryTransLocalBlackChickenData': {
            '黑羽土雞舍飼(南區)公': '黑羽土雞（南區，公，舍飼）',
            '黑羽土雞舍飼(南區)母': '黑羽土雞（南區，母，舍飼）',
        },
    }

    @staticmethod
    def _process_raw_data(
        raw_data: List[Dict[str, str]],
        fields: Dict[str, str],
    ) -> Dict[str, List[Dict[str, Union[str, float]]]]:
        '''處理原始資料'''
        result = dict()
        for node in raw_data:
            date = node['日期']
            for field, name in fields.items():
                if name not in result:
                    result[name] = list()
                rawValue: str = node[field]
                # 排除例外狀況，例如值為空或「休市」等
                if rawValue != '休市' and rawValue != '-' and rawValue != '':
                    # 處理特殊狀況，例如小數點多一個點或以範圍的方式表示
                    if '..' in rawValue:
                        rawValue = rawValue.replace('..', '.')
                    if '-' in rawValue:
                        rawValues = rawValue.split('-')
                        rawValue = (
                            float(rawValues[0]) + float(rawValues[1])) / 2
                    value = float(rawValue)
                    if value > 0:
                        result[name].append({'date': date, 'value': value})
        return result

    @staticmethod
    def _gen_date_range(start_str: str, end_str: str) -> List[str]:
        '''產生範圍內所有日期的列表'''
        date_range = list()
        time = datetime.strptime(start_str, '%Y/%m/%d')
        end = datetime.strptime(end_str, '%Y/%m/%d')
        step = timedelta(days=1)
        while time <= end:
            date_range.append(time.strftime('%Y/%m/%d'))
            time += step
        return date_range

    @staticmethod
    def _get_data(key: Optional[str] = None) -> (
            Dict[str, List[Dict[str, Union[str, float]]]],
            Dict[str, np.ndarray]):
        '''取得資料'''

        def request_data(src: str):
            '''請求資料'''
            with urlopen(Handler._data_url.format(src)) as f:
                raw_data = json.load(f)
            return src, raw_data

        data, datasets = dict(), dict()
        # 去檢查是否只要抓一部分的資料
        if key is None:
            srcs = Handler._data_sources.keys()
        else:
            srcs = list()
            for src, fields in Handler._data_sources.items():
                if key in fields.values():
                    srcs.append(src)
        # 使用執行緒池同時做請求，加快抓取資料的速度
        results = ThreadPool(len(srcs)).imap(request_data, srcs)
        for src, raw_data in results:
            fields = Handler._data_sources[src]
            for k, v in Handler._process_raw_data(raw_data, fields).items():
                if k in data:
                    v.extend(data[k])
                data[k] = v
        # 從處理好的資料製作方便機器學習使用的資料集
        for k, v in data.items():
            date_range = Handler._gen_date_range(
                v[-1]['date'], datetime.now().strftime('%Y/%m/%d'))
            dataset = np.empty(len(date_range))
            nodes = v[::-1]
            for i, node in enumerate(nodes):
                start = date_range.index(node['date'])
                if i < len(nodes) - 1:
                    end = date_range.index(nodes[i+1]['date'])
                else:
                    end = len(date_range)
                dataset[start:end] = node['value']
            datasets[k] = dataset
        return data, datasets

    @staticmethod
    def _train_and_predict(
            dataset: np.ndarray, past: int, future: int) -> List[float]:
        '''訓練模型並且預測'''
        l = len(dataset)
        x = np.arange(l - past, l).reshape(-1, 1)
        x_pred = np.arange(l - past, l + future).reshape(-1, 1)
        y = dataset[-past:]
        svr = SVR(kernel='rbf', C=20).fit(x, y)
        return y.tolist() + svr.predict(x_pred).flatten().tolist()

    def _set_send_json_response(self):
        '''設置回傳JSON時需要的回應'''
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json; charset=UTF-8')
        self.end_headers()

    def __init__(self, *args, directory=None, **kwargs):
        '''初始化'''
        self._data: Dict[str, List[Dict[str, Union[str, float]]]] = None
        self._datasets: Dict[np.ndarray] = None
        # 設置伺服器起始資料夾的路徑
        directory = path.join(path.dirname(__file__), '../../dist')
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        '''做GET請求'''
        if self.path == '/api/data':
            # 取得資料時的API之處理
            data, _ = Handler._get_data()
            self._set_send_json_response()
            self.wfile.write(
                json.dumps(data, ensure_ascii=False).encode('utf-8'))
        elif self.path.startswith('/api/pred'):
            # 做預測時的API之處理
            try:
                query = parse_qs(urlparse(self.path).query)
                # 檢查參數是否合法
                key = query['key'][0]
                past = int(query['past'][0])
                future = int(query['future'][0])
                _, datasets = Handler._get_data(key)
                dataset = datasets[key]
                assert 0 < past <= len(dataset) and future > 0
            except:
                super().do_GET()
                return
            pred = Handler._train_and_predict(dataset, past, future)
            self._set_send_json_response()
            self.wfile.write(json.dumps(
                pred, ensure_ascii=False).encode('utf-8'))
        else:
            super().do_GET()


def run_server():
    '''執行伺服器'''
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.serve_forever()
