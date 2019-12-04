from __future__ import print_function, division
from keras.datasets import mnist
from keras_contrib.layers.normalization.instancenormalization import InstanceNormalization
from keras.layers import Input, Dense, Reshape, Flatten, Dropout, Concatenate
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.models import Sequential, Model
from keras.optimizers import Adam
import datetime
import matplotlib.pyplot as plt
import sys
import numpy as np
import os
from static.vendor.core.DataLoader import DataLoader
from keras.models import load_model
import keras_contrib
from PIL import Image
import scipy.misc

class CycleGAN():
    def __init__(self):
        #cargando el modelo entrenado
        self.data_loader=DataLoader(img_resolution=(256, 256))

        self.model_route="./static/vendor/core/saved_models/"

        self.g_BA = load_model(self.model_route + "facades/g_BA_complete_model_256.h5", custom_objects={'InstanceNormalization':keras_contrib.layers.InstanceNormalization})

        self.g_BA._make_predict_function()

        print("Modelo cargado correctamente")


    def generate_image(self, filename):

        imgs_B = self.data_loader.load_img(filename)

        fake_A = self.g_BA.predict(imgs_B)

        gen_imgs = np.concatenate([fake_A])

        fake_A = 0.5 * fake_A + 0.5

        #print(fake_A)

        fig, axs = plt.subplots()
        axs.imshow(fake_A[0])
        axs.set_title('Generada')
        axs.axis('off')

        fig.savefig("./static/assets/generated.png")
        plt.close()
        