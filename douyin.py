# -*- coding:utf-8 -*-
import json
import re
import sys
from subprocess import PIPE, Popen

import requests


class DouYin(object):
    def __init__(self, width=500, height=300):
        rip = '183.14.108.84'
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
            'X-Real-IP': str(rip),
            'X-Forwarded-For': str(rip),
        }

    def format_data(self, aweme):
        statistics = aweme['statistics']
        video = aweme['video']

        up_count = str(statistics['digg_count'])
        data = {
            'video_id': aweme['aweme_id'],
            'source': 'douyin',
            'content': aweme['share_info']['share_desc'].encode('utf-8'),
            'topic': '',
            'comment_count': 0,
            'share_count': 0,
            'up_count': up_count if 'w' not in up_count else str(float(up_count[0:-1]) * 10000),  # 该字段内容格式举例：7.2w，表示72000
            'down_count': 0,
            'play_count': 0,
            'duration': 0,  # 没有相关字段？
            'width': video['width'],
            'height': video['height'],
            'video_url': video['play_addr']['url_list'][0].replace('playwm', 'play'),  # playwm 有水印，替换为 play 无水印
            'pic_url': video['cover']['url_list'][0]
        }
        return data

    def get_video_urls(self, uid):
        aweme_count = 32767  # html['user_list'][0]['user_info']['aweme_count']
        share_user_url = 'https://www.amemv.com/share/user/%s' % uid
        share_user = requests.get(
            share_user_url, headers=self.headers, verify=False)
        _dytk_re = re.compile(r"dytk: '(.+)'")
        dytk = _dytk_re.search(share_user.text).group(1)
        try:
            process = Popen(['node', 'byted-acrawler.js', str(uid)], stdout=PIPE, stderr=PIPE)
        except (OSError, IOError) as err:
            print('请先安装 node.js: https://nodejs.org/')
            sys.exit()
        sign = process.communicate()[0].decode().strip('\n')
        user_url = 'https://www.amemv.com/aweme/v1/aweme/post/?user_id=%s&max_cursor=0&count=%s&aid=1128&_signature=%s&dytk=%s' % (
            uid, aweme_count, sign, dytk)
        req = requests.get(user_url, headers=self.headers, verify=False)
        html = json.loads(req.text)

        results = []
        for aweme in html['aweme_list']:
            results.append(self.format_data(aweme))
        return results

    def run(self):
        user_id = '82033562459'
        print(len(self.get_video_urls(user_id)))


if __name__ == '__main__':
    douyin = DouYin()
    douyin.run()
