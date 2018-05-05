import sys
import os
from PIL import Image
from io import BytesIO

import pandas as pd
import requests

from skimage.io import imread
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.getcwd(), "src"))
from ecallen.ecallen import images as ecimg


# http://help.brain-map.org/display/api/Downloading+an+Image
# to download an image
image_base = 'http://api.brain-map.org/api/v2/section_image_download'


def get_organism_image_params(organism):
    if organism == 'DevMouse':
        image_params = {'left':2000, 'top':1000, 'width':5000, 'height':5000}
    else:
        image_params = None
    return image_params


def get_image(image_id, image_params=None):
    q = image_base + '/' + str(image_id)
    if image_params is not None:
        # olfactory bulb is in the top left corner of the image
        image_c = '&'.join([param + '=' + str(pxls) for param, pxls in image_params.items()])
        # query cropped image
        q = q + '?' + image_c
    print('\tattempting query:', q)
    r = requests.get(q, stream=True)
    return Image.open(BytesIO(r.content))


def save_image_locally(image_dir, image_id, image_num,  image_params=None):
    image_filepath = os.path.join(image_dir, str(image_num) + '_' + str(image_id) + '.jpg')
    img = get_image(image_id, image_params=image_params)
    img.save(image_filepath)
    return image_filepath