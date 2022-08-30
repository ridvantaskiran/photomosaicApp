import glob
import math
from PIL import Image
import numpy as np


def rgb(image):
    im1 = Image.Image.split(image)

    r = np.array(im1[0])
    g = np.array(im1[1])
    b = np.array(im1[2])
    return r, g, b


def imageLoad(image):
    img = Image.open(image)
    y = img.resize((108, 108))
    # imgSmall = y.resize((50, 50), resample=Image.BILINEAR)
    # result = imgSmall.resize(y.size, Image.NEAREST)

    r, g, b = rgb(y)

    source_images = sourceImg('smallchair')

    back = Image.open('white_background.jpg')
    back_im = back.resize((1080, 1080)).copy()

    for row in range(108):
        for col in range(108):
            max_dist = 255
            for i in range(len(source_images)):

                dist = math.sqrt((r[row][col] - source_images[i][0]) ** 2 + (g[row][col] - source_images[i][1]) ** 2 + (
                        b[row][col] - source_images[i][2]) ** 2)
                if dist < max_dist:
                    max_dist = dist
                    index = i
            im2 = Image.open('smallchair/img' + str(index) + '.jpg')
            back_im.paste(im2, (col * 10, row * 10))
    back_im.save('output.jpg')


def sourceImg(path):
    image_list_r = []
    image_list_g = []
    image_list_b = []
    for filename in glob.glob(path + '/*.jpg'):  # assuming gif
        im = Image.open(filename)
        im1 = Image.Image.split(im)
        r = np.array(im1[0])
        g = np.array(im1[1])
        b = np.array(im1[2])

        pixR = np.average(r)
        image_list_r.append(pixR)

        pixG = np.average(g)
        image_list_g.append(pixG)

        pixB = np.average(b)
        image_list_b.append(pixB)
    image = list(zip(image_list_r, image_list_g, image_list_b))
    return image


def sourceGenerator(data):
    i = 0
    for filename in glob.glob(data + '/*'):
        name = 'img' + str(i) + '.jpg'
        im = Image.open(filename)
        img = im.convert('RGB')
        img = img.resize((10, 10))
        img.save('smallchair/' + name)
        i += 1


imageLoad('input.jpg')