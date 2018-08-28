# -*- coding: utf-8 -*-

import qiniu
import requests

accessKey = "sFh8m4CIWG1kzMhz0lcwi5E3mJ9Dq8U-sjNmYYey"
secretKey = "zzUOkj6ELFys1jITX_qMLKWBnRi4aJ-jNpO2B6aT"
bucket = "qiubai-circle"
bucket = 'qiushibaike'
auth = qiniu.Auth(accessKey, secretKey)
manager = qiniu.BucketManager(auth)


def upload(file, key):
    up_token = auth.upload_token(bucket)
    _, response = qiniu.put_file(up_token, key, file)
    print response


def refresh(urls):
    data = {'urls': urls}
    post_url = 'http://fusion.qiniuapi.com/refresh'
    token = auth.token_of_request(post_url)
    headers = {'Content-Type': 'application/json', 'Authorization': 'QBox {0}'.format(token)}
    response = requests.post(post_url, json=data, headers=headers)
    print '*' * 5, response.json()


if __name__ == "__main__":
    urls = []
    upload('top_logo.png', 'share/images/qbshare/banner.png')

