# -*- coding: utf-8 -*-

import sys
import os
import shutil
import subprocess
import time
from PIL import Image

webp_cmd = '/home/ids/Workspace/libwebp-1.0.0-rc3-linux-x86-64/bin/cwebp'


def process(arg):
    # 1. 获取所有要切图文件的列表
    # 2. 依次遍历、备份文件
    # 3. 切图
    # 4. 测试
    # 5. 刷新 CDN
    path = os.path.abspath(arg)
    print('%s start processing...' % path)

    for root, dirs, files in os.walk(path):
        for file in files:
            f = os.path.join(root, file)

            if 'small' not in f:
                continue

            if f.endswith('jpg') or f.endswith('jpeg'):
                # 最近 30 天的才处理
                if time.time() - os.stat(f).st_ctime > 2678400:
                    continue

                shutil.copyfile(f, f + '.bak')  # 备份
                im = Image.open(f)
                width, height = im.size

                if height / width <= 3:
                    continue

                crop_h = width / 0.46
                subprocess.call([
                    'convert', f, '-crop', '%dx%d+0+0' % (width, crop_h), f
                ])
                print('croped: %s' % f)

                subprocess.call([webp_cmd, f, '-o', f.split('.')[0] + '.webp'])
                print('webp generated: %s', f)


if __name__ == '__main__':
    process(sys.argv[1])
