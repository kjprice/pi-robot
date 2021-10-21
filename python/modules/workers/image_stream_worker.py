import multiprocessing
import time

import imagezmq

LOCAL_PUB_SUB = False

def image_stream_worker(images, image_hub_url):
    print('Image stream worker Connecting to', image_hub_url)
    image_hub = imagezmq.ImageHub(open_port=image_hub_url, REQ_REP=False)

    while True:
      camera_timestamp, image_found = image_hub.recv_image()
      images.insert(0, (image_found, time.time(), camera_timestamp))
      if len(images) > 2:
          images.pop()

def get_perpetual_list_of_images_from_worker(image_hub_url):
    mgr = multiprocessing.Manager()
    images = mgr.list()
    job = multiprocessing.Process(
            target=image_stream_worker,
            args=(images, image_hub_url),
        )
    job.start()

    return images
