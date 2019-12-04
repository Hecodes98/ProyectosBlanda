from __future__ import print_function, division
import scipy
from glob import glob
import numpy as np
import scipy.misc

class DataLoader:
    def __init__(self, img_resolution=(256, 256)):
        self.img_resolution=img_resolution

    def load_data(self):
        img = self.imread("img.jpg")
        #img = scipy.misc.imresize(img, self.img_resolution)

        imgs=[]
        imgs.append(img)

        imgs = np.array(imgs)/127.5 - 1.
        
        return imgs


    def load_img(self, path):
        img = self.imread(path)
        img = scipy.misc.imresize(img, self.img_resolution)
        img = img/127.5 - 1.
        return img[np.newaxis, :, :, :]


    def imread(self, path):
        return scipy.misc.imread(path, mode='RGB').astype(np.float)
