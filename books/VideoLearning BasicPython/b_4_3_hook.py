import requests


def get_info(response, *args, **kwargs):
    '''
    回调函数
    '''
    print(response.headers['Content-Type'])


def main():
    '''
    主程序
    '''
    requests.get('https://www.baidu.com', hooks=dict(response=get_info))


if __name__ == '__main__':
    main()

"""
事件钩子：
程序发出一个IO请求，等请求返回后自动进行回调处理
"""