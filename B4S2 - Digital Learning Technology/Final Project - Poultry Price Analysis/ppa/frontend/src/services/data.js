import axios from 'axios';

/*
import { getDateString } from '@/utils';

const dataSources = new Map([
  [
    'PoultryTransBoiledChickenData',
    new Map([
      ['白肉雞(2.0Kg以上)', '白肉雞（2.0kg以上）'],
      ['白肉雞(1.75-1.95Kg)', '白肉雞（1.75~1.95kg）'],
      ['白肉雞(門市價高屏)', '白肉雞（門市價，高屏）'],
      ['雞蛋(產地)', '雞蛋（產地）'],
    ]),
  ],
  [
    'PoultryTransLocalChickenData',
    new Map([
      ['黑羽土雞公舍飼', '黑羽土雞（南區，公，舍飼）'],
      ['黑羽土雞母舍飼', '黑羽土雞（南區，母，舍飼）'],
    ]),
  ],
  [
    'PoultryTransGooseDuckData',
    new Map([
      ['肉鵝(白羅曼)', '肉鵝（白羅曼）'],
      ['正番鴨(公)', '正番鴨（公）'],
      ['土番鴨(75天)', '土番鴨（75天）'],
      ['鴨蛋(新蛋)(台南)', '鴨蛋（新蛋，台南）'],
    ]),
  ],
  [
    'PoultryTransLocalRedChickenData',
    new Map([
      ['紅羽土雞北區', '紅羽土雞（北區）'],
      ['紅羽土雞中區', '紅羽土雞（中區）'],
      ['紅羽土雞南區', '紅羽土雞（南區）'],
    ]),
  ],
  [
    'PoultryTransLocalBlackChickenData',
    new Map([
      ['黑羽土雞舍飼(南區)公', '黑羽土雞（南區，公，舍飼）'],
      ['黑羽土雞舍飼(南區)母', '黑羽土雞（南區，母，舍飼）'],
    ]),
  ],
]);

function getDataUrl(src) {
  const url = 'https://cors-anywhere.herokuapp.com/';
  return url + `https://data.coa.gov.tw/Service/OpenData/FromM/${src}.aspx`;
}

function processRawData(rawData, fields) {
  const result = new Map();
  for (const node of rawData) {
    const date = node['日期'];
    for (const [field, name] of fields) {
      if (!result.has(name)) result.set(name, new Array());
      let rawValue = node[field];
      if (rawValue != '休市' && rawValue != '-' && rawValue != '') {
        if (rawValue.includes('..')) rawValue = rawValue.replace('..', '.');
        if (rawValue.includes('-')) {
          const rawValues = rawValue.split('-');
          rawValue = (Number(rawValues[0]) + Number(rawValues[1])) / 2;
        }
        const value = Number(rawValue);
        if (value > 0) result.get(name).push({ date: date, value: value });
      }
    }
  }
  return result;
}
*/

let data = new Map(); // 資料

// 取得資料
export function getData() {
  return axios.get('/api/data').then((response) => {
    for (const [k, v] of Object.entries(response.data)) data.set(k, v);
  });
  /*
  const date = getDateString();
  if (date === localStorage.getItem('date')) {
    return new Promise((resolve) => {
      JSON.parse(localStorage.getItem('data')).forEach(([k, v]) =>
        data.set(k, v)
      );
      resolve();
    });
  }
  return Promise.all(
    Array.from(dataSources).map(async ([src, fields]) => {
      axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
      const response = await axios.get(getDataUrl(src));
      return processRawData(response.data, fields);
    })
  ).then((results) => {
    results.forEach((result) =>
      result.forEach((v, k) => {
        if (!data.has(k)) data.set(k, v);
        else data.set(k, [...data.get(k), ...v]);
      })
    );
    localStorage.setItem('date', date);
    localStorage.setItem('data', JSON.stringify(Array.from(data)));
  });
  */
}

// 取得預測結果
export function getPrediction(key, past, future) {
  return axios
    .get('/api/pred', { params: { key, past, future } })
    .then((response) => response.data)
    .catch(() => null);
}

export const dataUnit = '元／台斤'; // 資料單位

export const dataItems = [ // 資料顯示在網頁畫面上的元素
  {
    key: '01',
    icon: '🐔',
    title: '白肉雞（2.0kg以上）',
  },
  {
    key: '02',
    icon: '🐔',
    title: '白肉雞（1.75~1.95kg）',
  },
  {
    key: '03',
    icon: '🐔',
    title: '白肉雞（門市價，高屏）',
  },
  {
    key: '04',
    icon: '🥚',
    title: '雞蛋（產地）',
  },
  {
    key: '05',
    icon: '🦢',
    title: '肉鵝（白羅曼）',
  },
  {
    key: '06',
    icon: '🦆',
    title: '正番鴨（公）',
  },
  {
    key: '07',
    icon: '🦆',
    title: '土番鴨（75天）',
  },
  {
    key: '08',
    icon: '🥚',
    title: '鴨蛋（新蛋，台南）',
  },
  {
    key: '09',
    icon: '🐓',
    title: '紅羽土雞（北區）',
  },
  {
    key: '10',
    icon: '🐓',
    title: '紅羽土雞（中區）',
  },
  {
    key: '11',
    icon: '🐓',
    title: '紅羽土雞（南區）',
  },
  {
    key: '12',
    icon: '🐓',
    title: '黑羽土雞（南區，公，舍飼）',
  },
  {
    key: '13',
    icon: '🐓',
    title: '黑羽土雞（南區，母，舍飼）',
  },
];

export default data;
