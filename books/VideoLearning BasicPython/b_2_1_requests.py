import json
import requests
from requests.exceptions import Timeout, HTTPError

URL = "https://api.github.com"


def make_url(endpart):
    return '/'.join([URL, endpart])


def indent_format(jsonStr):
    return json.dumps(json.loads(jsonStr), indent=4)


def request_method(endpart_url):
    url = make_url(endpart_url)
    print(f"url:{url}")
    # response = requests.get(url,auth=('imoocdemo','imoocdemo123'))
    response = requests.get(url, auth=('username', 'password'))
    # print(response.text)
    print(indent_format(response.text))


def requests_params():
    '''
    带参数的请求
    :return: 格式化的response
    '''
    response = requests.get(make_url('user'), auth=('imoocdemo', 'imoocdemo123'), params={'since': 11})
    print(response.url)
    print(indent_format(response.text))
    print(response.request.headers)


def requests_json():
    # patch：
    # response = requests.patch(make_url('user'), auth=('username', 'password'),
    #                           json={'blog': 'https://blog.csdn.net/qq_31362767',
    #                                 'company': 'Uniview'})
    # post：
    response = requests.post(make_url('user/emails'), auth=('username', 'password'),
                             json=["15779786901@163.com", "zhuyuping@uniview.com"])
    print(response.url)
    print(indent_format(response.text))
    print(response.request.headers)
    print(response.request.body)


def timeout_requests():
    try:
        response = requests.get(make_url('user/emails'), auth=('username', 'password'), timeout=0.1)
        response.raise_for_status()
    except Timeout as e:
        print('Timeout:', e)
    except HTTPError as e:
        print('HTTPError:', e)
    else:
        print(indent_format(response.text))


if __name__ == '__main__':
    # res = request_method('user/emails')  # 获取邮箱的get请求
    # requests_params()   # 携带参数的get请求
    # requests_json()     # patch、post请求
    timeout_requests()    # 异常处理
