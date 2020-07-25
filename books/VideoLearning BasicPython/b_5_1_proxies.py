
import requests
'''
代理：
pip3 install requests[socksv5]
'''

my_proxies={"http":"http://127.0.0.1:1080","https":"https://127.0.0.1:1080"}
# resp=requests.get("http://www.baidu.com",timeout=5)
# print(resp.text)

resp_proxies=requests.get("http://www.baidu.com",proxies=my_proxies,timeout=5)
print(resp_proxies.text)