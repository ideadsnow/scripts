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
    # for file in ['hot.png', 'prefer.png', 'promote.png']:
    #     typo = file.split('.')[0]
    #     for pl in ['ios', 'android']:
    #         key = 'sub_{}_{}_night.png'.format(pl, typo)
    #         print '*' * 3, manager.delete(bucket, key)
    #         upload(file, key)
    #         urls.append('http://pic.qiushibaike.com/{}'.format(key))
    #         urls.append('https://pic.qiushibaike.com/{}'.format(key))
    for id in ['120747119', '120747128', '120747130', '120747132', '120747179']:
        for t in ['small', 'medium']:
            key = 'system/pictures/12074/%s/%s/app%s.jpeg' % (id, t, id)
            urls.append('https://pic.qiushibaike.com/%s' % key)
    print urls
    refresh(urls)
