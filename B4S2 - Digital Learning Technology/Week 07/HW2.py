import os
import re
from urllib.parse import urljoin

import requests

POKEMON_BASE_URL = 'https://pokemon.wingzero.tw/'
POKEMON_GENN_URL = POKEMON_BASE_URL+'pokedex/generation/{}/tw'
POKEMON_ASST_URL = 'https://pokemon.wingzero.tw/assets/pokemon/{:03d}.png'


def main():
    pattern = re.compile(
        r'<a href="/pokedex/intro/(\d+?)/tw"><span class="pm_name">(.+?)'
        r'</span></a></h4>\s+?<div class="d-flex">\s+?<span[\S\s]+?><a>'
        r'(.+?)</a></span>(\s+?<span[\S\s]+?><a>(.+?)</a></span>)?\s+?</div>'
    )
    for i in [1, 5]:
        dir_path = f'Pokemon/Generation_{i}'
        os.makedirs(dir_path)
        url = POKEMON_GENN_URL.format(i)
        with requests.get(url) as r:
            if r.status_code != 200:
                r.raise_for_status()
            content = r.text
        for matches in pattern.findall(content):
            num, name = int(matches[0]), matches[1]
            attrs = matches[2]
            if matches[4] != '':
                attrs += ',' + matches[4]
            img_url = POKEMON_ASST_URL.format(num)
            img_path = os.path.join(dir_path, f'{num:03d}_{name}_{attrs}.png')
            r = requests.get(img_url, stream=True)
            if r.status_code == 200:
                with open(img_path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)


if __name__ == '__main__':
    main()
