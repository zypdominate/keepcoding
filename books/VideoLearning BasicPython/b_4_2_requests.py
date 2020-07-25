import requests


def download_picture():
    url = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1567621764963&di=6faf0c74a4b869979b6bddc20a65577b&imgtype=0&src=http%3A%2F%2Fpic.eastlady.cn%2Fuploads%2Ftp%2F201707%2F9999%2F45c57bd601.jpg'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    response = requests.get(url, headers=headers)
    print(response.headers)
    with open('demo.jpg', 'wb') as f:
        for chunk in response.iter_content(128):
            f.write(chunk)


from contextlib import closing
# 使用contextlib管理上下文，在打开后关闭流

def download_picture_stream():
    url = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1567621764963&di=6faf0c74a4b869979b6bddc20a65577b&imgtype=0&src=http%3A%2F%2Fpic.eastlady.cn%2Fuploads%2Ftp%2F201707%2F9999%2F45c57bd601.jpg'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    with closing(requests.get(url, headers=headers, stream=True)) as response:
        with open('demo1.jpg', 'wb') as f:
            for chunk in response.iter_content(128):
                f.write(chunk)


if __name__ == '__main__':
    # download_picture()
    download_picture_stream()
