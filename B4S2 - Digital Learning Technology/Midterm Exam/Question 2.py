import re

import requests


def main():
    with requests.get('http://sys.ndhu.edu.tw/AA/CLASS/subjselect/Default.aspx') as r:
        if r.status_code != 200:
            r.raise_for_status()
        content = r.text
    content = re.findall(r'<table class="date">([\S\s]+?)</table>', content)[0]
    table = {}
    for _, i, v, _ in re.findall(r'<(span|a) id="ContentPlaceHolder1_Label(\d+)">(.+?)</(span|a)>', content):
        i, j = int(i[:-1]), int(i[-1])
        if i not in table:
            table[i] = {}
        table[i][j] = re.sub(r'<.+?>', '', v)
    for _, v in table.items():
        if 3 in v:
            print(f'{v[1]}\t{v[2]}\t{v[3]}')


if __name__ == '__main__':
    main()
