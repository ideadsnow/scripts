import os
from PIL import Image

watermark = os.path.join('watermark.png')

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
    width, height = info['width'], info['height']
    is_width, short_side, long_side, rate = (True, height, width, width / height) \
        if width >= height else (False, width, height, height / width)
    value = min(9999, long_side) if rate >= 3 else min(1080, width)
    scale = "{}:-1".format(value) if (rate >= 3 and is_width) or \
        (rate < 3 and not is_width) else "-1:{}".format(value)
    rate = 6
    w_exp = 'if(gt(iw, ih), oh*main_a, min(iw, ih)/%s)' % rate
    h_exp = 'if(gt(iw, ih), min(iw, ih)/%s, ow/main_a)' % rate
    w_exp, h_exp = 'min(iw, ih)/%s' % rate, 'ow/main_a'
    w_pos = 'main_w-overlay_w-\'min(H, W)\'/30'
    h_pos = 'main_h-overlay_h-\'min(H, W)\'/50'
    cmd = '%s -i %s -i %s -filter_complex \
        "[0:v]scale=%s[a];[1][a]scale2ref=\'%s\':\'%s\'[wm][vid];[vid][wm]overlay=%s:%s[out];\
        [out]scale=trunc(iw/2)*2:trunc(ih/2)*2[rs]" -map "[rs]" -y %s'
    command = cmd % ('ffmpeg', filename, watermark, scale, w_exp, h_exp, w_pos, h_pos, output)
    print command
    p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
    return p.wait()

process_image('0DT52M11D7WXWTUG', '0DT52M11D7WXWTUG.jpg')