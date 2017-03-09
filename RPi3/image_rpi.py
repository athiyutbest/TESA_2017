import os
import sys
from PIL import Image

SIZE = 1024, 1024
SIZE_MINI = 240, 240


def resize_image(image):
    cwd = os.getcwd()
    outfile = os.path.splitext(image)[0] + '_preview' + ".jpg"
    try:
        im = Image.open(image)
        im.thumbnail(SIZE_MINI, Image.ANTIALIAS)
        im.save(outfile, "JPEG")
    except IOError:
        print("cannot create resized file")
