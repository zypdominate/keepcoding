from concurrent import futures
from a5_4_downloadimage import save_image, get_image, show, main

MAX_WORDERS = 20

def download_single(image_name):
    image = get_image(image_name)
    save_image(image, image_name)
    show(image)
    return image_name

def download_multiple(image_name_list):
    tasks = min(MAX_WORDERS, len(image_name_list))
    with futures.ThreadPoolExecutor(tasks) as executor:
    # with futures.ProcessPoolExecutor() as executor:
        res = executor.map(download_single, sorted(image_name_list))
    return len(list(res))

if __name__ == '__main__':
    main(download_multiple)

# download 80 images in 1.4081335067749023s
# download 80 images in 1.561039924621582s
# download 80 images in 1.393141746520996s