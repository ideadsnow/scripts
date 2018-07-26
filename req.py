import requests

headers = {
    'Host': 'm2-test3.qiushibaike.com',
    'Uuid': 'ios_0a5b41dca8c7a34059718870a49e0cccd74e4e59',
    'qbid': '38701989',
    'Qbtoken': 'df9f884f6e0fa8164a4b3bc0731899a9cc5dcef1',
    'Accept': '*/*',
    'Source': 'ios_11.0.4',
    'Content-Type': 'multipart/form-data',
    'Accept-Language': 'zh-Hans;q=1',
    'app': '1',
    'Accept-Encoding': 'br, gzip, deflate',
    'Content-Length': '256',
    'User-Agent': 'QiuBai/11.0.4 rv:8 (iPhone; iOS 11.4; zh_CN) PLHttpClient/1_WIFI',
    'qbaid': '206C8033-8BBC-4133-9709-9813E7CE0677',
    'Connection': 'keep-alive',
}

url = 'http://m2-test3.qiushibaike.com/article/create'

params = {}
#  data = {
    #  'json': [{
        #  'screen_height':1334,
        #  'attachments':['article/image/RKTEC1BXSHGZ2BCD'],
        #  'content':'dghff',
        #  'allow_comment':'true',
        #  'screen_width':750,
        #  'anonymous':'false'
    #  }]
#  }
data = {}


rep = requests.post(url, params=params, headers=headers, verify=False, data=data, files={'file': open('a', 'rb')})

print rep.json()
