import os
import sys
import time
import requests

DOWNNLOAD_DIR = r'D:\downloadimage'
BASE_URL = 'http://pic2.sc.chinaz.com/Files/pic/pic9/202002/'
image_list = ['zzpic231' + str(i) + '_s.jpg' for i in range(10, 90)]


def save_image(img, filename):
    path = os.path.join(DOWNNLOAD_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

def get_image(suffix):
    url = os.path.join(BASE_URL, suffix)
    response = requests.get(url)
    return response.content

def show(text):
    print(text,end='\n')
    sys.stdout.flush()

def download_all(image_name_list):
    for image_name in image_name_list:
        image = get_image(image_name)
        save_image(image, image_name)
        show(image)
    return len(image_name_list)

def main(download_task):
    t0 = time.time()
    count = download_task(image_list)
    elapsed = time.time() - t0
    msg = f'\n download {count} images in {elapsed}s'
    print(msg)

if __name__ == '__main__':
    main(download_all)

#  download 80 images in 4.6661295890808105s
#  download 80 images in 5.478628873825073s
#  download 80 images in 4.028514862060547s

























