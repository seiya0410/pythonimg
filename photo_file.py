import os
from PIL import Image

#set the path
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = BASE_DIR + '/data/photos.sqlite3'
FILES_DIR = BASE_DIR + '/files'

#return the path to save the image
def get_path(file_id, ptype = ''):
    return FILES_DIR + '/' + str(file_id) + ptype + '.jpg'

#thumb nail
def make_thumbnail(file_id, size):
    src = get_path(file_id)
    des = get_path(file_id, '-thumb')
    #do not create a thumbnail if it exists
    if os.path.exists(des): return des
    #squire 
    img = Image.open(src)
    msize = img.width if img.width < img.height else img.height
    img_crop = image_crop_center(img, msize)
    #resize it
    img_resize = img_crop.resize((size, size))
    img_resize.save(des, quality=95)
    return des

#cut the center of image as squre
def image_crop_center(img, size):
    cx = int(img.width / 2)
    cy = int(img.height / 2)
    img_crop = img.crop((
        cx - size / 2, cy - size /2,
        cx + size /2, cy + size / 2))
    return img_crop