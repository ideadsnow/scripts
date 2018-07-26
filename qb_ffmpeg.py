import os
import subprocess
from PIL import Image

ffmpeg_cmd = '/usr/local/bin/ffmpeg'
watermark = 'watermark.png'


def get_image_info(filename):
    image = Image.open(filename)
    return {
        'width': image.width,
        'height': image.height,
        'format': image.format.lower(),
        'size': os.path.getsize(filename)
    }


def process_image(filename, output):
    info = get_image_info(filename)
    print info
    width, height = info['width'], info['height']
    is_width, short_side, long_side, rate = (True, height, width, width / height) \
        if width >= height else (False, width, height, height / width)
    value = min(9999, long_side) if rate >= 3 else min(1080, width)
    scale = "{}:-1".format(value) if (rate >= 3 and is_width) or \
        (rate < 3 and not is_width) else "-1:{}".format(value)
    crop_h = 'ih'
    if not is_width and rate >= 3:
        crop_h = 900
    rate = 6
    w_exp = 'if(gt(iw, ih), oh*main_a, min(iw, ih)/%s)' % rate
    h_exp = 'if(gt(iw, ih), min(iw, ih)/%s, ow/main_a)' % rate
    w_exp, h_exp = 'min(iw, ih)/%s' % rate, 'ow/main_a'
    w_pos = 'main_w-overlay_w-\'min(H, W)\'/30'
    h_pos = 'main_h-overlay_h-\'min(H, W)\'/50'

    cmd = '%s -i %s -i %s -filter_complex \
        "[0:v]scale=%s[a];[1][a]scale2ref=\'%s\':\'%s\'[wm][vid];[vid]crop=iw:%s[crop];[crop][wm]overlay=%s:%s[out];\
        [out]scale=trunc(iw/2)*2:trunc(ih/2)*2[rs]" -map "[rs]" -y %s'
    command = cmd % (ffmpeg_cmd, filename, watermark, scale, w_exp, h_exp, crop_h, w_pos, h_pos, output)
    print command
    exit(0)

    p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
    p.wait()


#src = 'sss.jpg'
src = '/Users/ids/Workspace/t/P4OEWDU53DMWYH21'
target = 'tttt.jpg'

process_image(src, target)
