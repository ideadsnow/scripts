# -*- coding: utf-8 -*-

import requests
from qiniu import Auth

accessKey = "sFh8m4CIWG1kzMhz0lcwi5E3mJ9Dq8U-sjNmYYey"
secretKey = "zzUOkj6ELFys1jITX_qMLKWBnRi4aJ-jNpO2B6aT"
bucket = "qiubai-circle"
auth = Auth(accessKey, secretKey)
apk_key = 'qiushibaike.apk'
data = {'urls': ['http://circle-pic.qiushibaike.com/%s' % apk_key]}
post_url = 'http://fusion.qiniuapi.com/refresh'
token = auth.token_of_request(post_url)
headers = {'Content-Type': 'application/json', 'Authorization': 'QBox {0}'.format(token)}
response = requests.post(post_url, json=data, headers=headers)
print '<' * 15, response.json()
