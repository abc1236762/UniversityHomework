import re

import requests

USERNAME = ''
PASSWORD = ''

NDHU_CSS_URL = 'http://sys.ndhu.edu.tw/AA/CLASS/subjselect/Default.aspx'
NDHU_CSS_CH_URL = 'http://sys.ndhu.edu.tw/AA/CLASS/subjselect/course_history.aspx'


def get_basic_post_data(content):
    view_state = re.search(
        r'id="__VIEWSTATE" value="(\S+?)"', content).group(1)
    view_state_generator = re.search(
        r'id="__VIEWSTATEGENERATOR" value="(\S+?)"', content).group(1)
    event_validation = re.search(
        r'id="__EVENTVALIDATION" value="(\S+?)"', content).group(1)
    return {
        '__VIEWSTATE': view_state,
        '__VIEWSTATEGENERATOR': view_state_generator,
        '__EVENTVALIDATION': event_validation,
    }


def main():
    s = requests.Session()
    cookies = requests.cookies.cookiejar_from_dict(dict())
    with s.get(NDHU_CSS_URL, cookies=cookies) as r:
        if r.status_code != 200:
            r.raise_for_status()
        content = r.text
    cookies = r.cookies
    btn_login = re.search(
        r'name="ctl00\$ContentPlaceHolder1\$BtnLogin" value="(\S+?)"',
        content).group(1)
    hve = re.search(
        r'id="ContentPlaceHolder1_hve" value="(\S+?)"', content).group(1)
    post_data = get_basic_post_data(content)
    post_data['ctl00$ContentPlaceHolder1$ed_StudNo'] = USERNAME
    post_data['ctl00$ContentPlaceHolder1$ed_pass'] = PASSWORD
    post_data['ctl00$ContentPlaceHolder1$BtnLogin'] = btn_login
    post_data['ctl00$ContentPlaceHolder1$hve'] = hve
    with s.post(NDHU_CSS_URL, post_data, cookies=cookies) as r:
        if r.status_code != 200:
            r.raise_for_status()
    cookies = r.cookies
    with s.get(NDHU_CSS_CH_URL, cookies=cookies) as r:
        if r.status_code != 200:
            r.raise_for_status()
        content = r.text
    cookies = r.cookies
    button3 = re.search(
        r'name="ctl00\$ContentPlaceHolder1\$Button3" value="(\S+?)"',
        content).group(1)
    post_data = get_basic_post_data(content)
    post_data['__EVENTTARGET'] = ''
    post_data['__EVENTARGUMENT'] = ''
    post_data['ctl00$ContentPlaceHolder1$Button3'] = button3
    with s.post(NDHU_CSS_CH_URL, data=post_data, cookies=cookies) as r:
        if r.status_code != 200:
            r.raise_for_status()
        content = r.text
    cookies = r.cookies
    with open('records.txt.html', 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    main()
