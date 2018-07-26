# -*- coding: utf-8 -*-
from qiniu import Auth, PersistentFop, build_op, op_save, urlsafe_base64_encode
import requests
import csv

url = 'http://pic.qiushibaike.com/'

access_key = 'sFh8m4CIWG1kzMhz0lcwi5E3mJ9Dq8U-sjNmYYey'
secret_key = 'zzUOkj6ELFys1jITX_qMLKWBnRi4aJ-jNpO2B6aT'
q = Auth(access_key, secret_key)

pipeline = 'qiushibaike'

bucket = to_bucket = 'qiushibaike'


def process(pid):
    r = requests.get('{}article/image/{}?imageInfo'.format(url, pid))
    r_json = r.json()
    if 'error' in r_json:
        return

    crop = ''
    if r_json['height'] / r_json['width'] > 3:
        crop = 'crop/x{}/'.format(r_json['width'] / 0.46)

    for fmt in ('webp', 'jpg'):
        key = 'article/image/{}.{}'.format(pid, fmt)
        to_key = 'article/image/{}_small.{}'.format(pid, fmt)

        saveas_key = urlsafe_base64_encode(to_bucket+':'+to_key)
        fops = 'imageMogr2/{}format/{}'.format(crop, fmt) + '|saveas/' + saveas_key

        pfop = PersistentFop(q, bucket, pipeline)
        ops = []
        ops.append(fops)
        ret, info = pfop.execute(key, ops, 1)
        print(info)
        print('{}{} done.'.format(url, to_key))


if __name__ == '__main__':
    with open('dump.sql', 'rb') as f:
        for line in f:
            print(line)
            process(line)
