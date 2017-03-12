import os
import sys
from PIL import Image

SIZE = 1024, 1024
SIZE_MINI = 240, 240
IMAGE_PATH = os.path.join(os.getcwd(), 'image')


def resize_image(image):
    cwd = os.getcwd()
    outfile = os.path.splitext(image)[0] + '_preview' + ".jpg"
    try:
        im = Image.open(image)
        im.thumbnail(SIZE_MINI, Image.ANTIALIAS)
        im.save(outfile, "JPEG")
    except IOError:
        print("cannot create resized file")


def remove_all_image():
    list_file = os.listdir(IMAGE_PATH)
    for file in list_file:
        os.remove(os.path.join(IMAGE_PATH, file))
    print("Succ : remove_all_image")


def get_image():
    list_image = os.listdir(IMAGE_PATH)
    tmp = []
    [tmp.append(os.path.join(IMAGE_PATH, image))
     for image in os.listdir(IMAGE_PATH)]
    return tmp
