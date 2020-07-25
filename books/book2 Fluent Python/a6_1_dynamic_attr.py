import os
import json
import warnings
import requests
from urllib.request import urlopen

URL = 'https://www.oreilly.com/pub/sc/osconfeed'
JSON_FILE = r'D:\keeplearning\myLearning\python\book2\osconfeed.json'


def load():
    if not os.path.exists(JSON_FILE):
        msg = f'downloading {URL} to {JSON_FILE}'
        warnings.warn(msg)
        with urlopen(URL) as remote, open(JSON_FILE, 'wb') as local:
            local.write(remote.read())
    # with open(JSON_FILE, mode='rb') as fp:
    with open(JSON_FILE, mode='r', encoding='utf8') as fp:
        return json.load(fp)


def load2():  # 还是使用 requests 吧
    if not os.path.exists(JSON_FILE):
        msg = f'downloading {URL} to {JSON_FILE}'
        warnings.warn(msg)
        with requests.get(URL) as remote, open(JSON_FILE, 'wb') as local:
            local.write(remote.content)
    with open(JSON_FILE, mode='r', encoding='utf8') as fp:
        return json.load(fp)


if __name__ == '__main__':
    # load()
    feed = load2()
    print(sorted(feed['Schedule'].keys()))
    # ['conferences', 'events', 'speakers', 'venues']

    for key, value in sorted(feed['Schedule'].items()):
        print(f'{len(value)},{key}')
    # 1,conferences
    # 494,events
    # 357,speakers
    # 53,venues
