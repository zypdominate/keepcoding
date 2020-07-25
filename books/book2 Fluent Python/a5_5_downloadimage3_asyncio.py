import os
import asyncio
import aiohttp
from a5_4_downloadimage import BASE_URL, save_image, show, main


@asyncio.coroutine
def get_image(suffix):
    url = os.path.join(BASE_URL, suffix)
    # response = yield from aiohttp.request('GET', url)
    response = yield from aiohttp.ClientSession().get(url)
    image = yield from response.read()
    return image


@asyncio.coroutine
def download_one(img):
    image = yield from get_image(img)
    show(img)
    save_image(image, filename=img)
    return img


def download_all(image_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(img) for img in sorted(image_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)


if __name__ == '__main__':
    main(download_all)
    #  download 80 images in 1.0823283195495605s
