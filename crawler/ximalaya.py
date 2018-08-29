import json
import random
import time
import requests
import aiohttp
import asyncio
import os
from bs4 import BeautifulSoup
from lxml import etree

DEST_DIR = 'audios/'

UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA_LIST)
}
headers2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.ximalaya.com/dq/all/2',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA_LIST)
}


category_urls = [
    'https://www.ximalaya.com/youshengshu/'
]

album_urls = [
    # 'https://www.ximalaya.com/youshengshu/14495260/',
    # 'https://www.ximalaya.com/xiangsheng/16313345/',
    # 'https://www.ximalaya.com/xiangsheng/3196/',
    # 'https://www.ximalaya.com/xiangsheng/8133373/',
    # 'https://www.ximalaya.com/xiangsheng/10218348/',
    # 'https://www.ximalaya.com/xiangsheng/3210/',

]

page_urls = []


def get_album_urls():
    for url in category_urls:
        html = requests.get(url, headers=headers2).text
        total_page_num = int(etree.HTML(html).xpath('(//ul[@class="Yetd pagination-page"]//span[@class="Yetd"])[last()]/text()')[0])
        print('{} 获取到的类别分页数：{}'.format(url, total_page_num))
        for num in range(1, total_page_num+1):
            sub_category_page = '{}p{}'.format(url, str(num))
            print('专辑 URL: {}'.format(sub_category_page))
            # 每个分类页获取专辑信息
            sub_html = requests.get(sub_category_page, headers=headers2).text
            temp_album_urls = ['https://www.ximalaya.com'+uri for uri in etree.HTML(html).xpath('//a[contains(concat(" ", @class, " "), "album-title")]/@href')]
            # print(temp_album_urls)
            album_urls.extend(temp_album_urls)
    print('获取到的全部专辑 URL 总数： {}'.format(len(album_urls)))


def get_page_urls():
    """获取 album_urls 中每个专辑的全部分页，并将子页面的 url 加入 page_urls 中"""
    for url in album_urls:
        html = requests.get(url, headers=headers2).text
        more_pages = etree.HTML(html).xpath('//a[@class="Yetd page-link"]/@href')
        total_page_num = len(more_pages)
        print('{} 获取到的专辑分页数：{}'.format(url, total_page_num))
        page_urls.extend(['{}p{}'.format(url, str(page_num)) for page_num in range(1, total_page_num+1)])
    print('待爬取的全部节目数： {}'.format(len(page_urls)))


async def fetch(url):
    """获取专辑页面"""
    async with aiohttp.ClientSession(headers=headers2) as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=3)) as html:
            try:
                response = await html.text(encoding="utf-8")
            except Exception as e:
                print(e)
                return
            return response


def save_file(fd, chunk):
    """被 download 调用"""
    fd.write(chunk)


async def download(url, path):
    """下载文件"""
    async with aiohttp.ClientSession(headers=headers2) as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as resp:
            with open(path, 'wb') as fd:
                while 1:
                    # 先注释掉，有 bug
                    # chunk = await resp.content.read(4096)
                    # if not chunk:
                    #     break
                    # lp = asyncio.get_event_loop()
                    # lp.run_in_executor(None, save_file, fd, chunk)
                    try:
                        chunk = await resp.content.read(4096)
                        if not chunk:
                            break
                        fd.write(chunk)
                    except Exception as e:
                        break
                        print(e)



# 获取专辑页面中曲目的 ids，并根据接口去获取
async def parser(sem, page_url):
    async with sem:
        try:
            html = await fetch(page_url)
        except Exception as e:
            print(e)
            return
        sound_urls = etree.HTML(html).xpath('//div[@class="dOi2 sound-list"]//div[@class="dOi2 text"]//a/@href')
        for url in sound_urls:
            sound_id = url.split('/')[-1]
            murl = 'http://www.ximalaya.com/tracks/{}.json'.format(sound_id)
            resp = requests.get(murl, headers=headers1)
            try:
                sound_info = resp.json()
            except Exception as e:
                continue
                # print(e)

            # print(sound_info)
            print(sound_info['play_path_64'])

            # 保存文件名格式：${DEST_DIR}/${album_id}/${sound_id}.${format}
            save_dir = os.path.join(DEST_DIR, str(sound_info['album_id']))
            os.makedirs(save_dir, exist_ok=True)
            try:
                path = os.path.join(save_dir, str(sound_info['id'])+'.'+sound_info['play_path_64'].split('.')[-1])
                await download(sound_info['play_path_64'], path)
            except Exception as e:
                print(e)
                continue
        print('{} 爬取完成'.format(page_url))


def write_list_to_file(l, path):
    with open(path, 'wb') as f:
        for e in l:
            f.write('{}\n'.format(e).encode())


if __name__ == '__main__':
    os.makedirs(DEST_DIR, exist_ok=True)
    start = time.time()

    get_album_urls()
    # 保存中间结果到文件，避免偶尔异常终端程序后又要重跑
    write_list_to_file(album_urls, 'album_urls')
    get_page_urls()
    # 保存中间结果到文件，避免偶尔异常终端程序后又要重跑
    write_list_to_file(page_urls, 'page_urls')

    # 异步爬虫，限制10个并发量
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(10)
    tasks = [parser(sem, url) for url in page_urls]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    end = time.time()
    print('耗时：', end-start)
