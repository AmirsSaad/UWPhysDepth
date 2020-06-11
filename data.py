import numpy as np
from utils import DepthNorm
from io import BytesIO
from PIL import Image
from zipfile import ZipFile
from tensorflow.keras.utils import Sequence
from augment import BasicPolicy
import pandas as pd
import os
import matplotlib.pyplot as plt

def extract_zip(input_zip):
    input_zip=ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

def nyu_resize(img, resolution=480, padding=6):
    from skimage.transform import resize
    return resize(img, (resolution, int(resolution*4/3)), preserve_range=True, mode='reflect', anti_aliasing=True )

def get_nyu_data(batch_size, nyu_data_zipfile=r'C:\Users\amirsaa\Desktop\D5.zip'):
    # data = extract_zip(nyu_data_zipfile)
    data = []
    nyu2_train = pd.read_csv(r'C:\Users\amirsaa\Documents\GitHub\DenseDepth\train_set.csv')
    nyu2_test = pd.read_csv(r'C:\Users\amirsaa\Documents\GitHub\DenseDepth\test_set.csv')

    shape_rgb = (batch_size, 480, 640, 3)
    shape_depth = (batch_size, 240, 320, 1)

    # Helpful for testing...
    if False:
        nyu2_train = nyu2_train[:10]
        nyu2_test = nyu2_test[:10]

    return data, nyu2_train, nyu2_test, shape_rgb, shape_depth

def get_nyu_train_test_data(batch_size):
    data, nyu2_train, nyu2_test, shape_rgb, shape_depth = get_nyu_data(batch_size)

    train_generator = NYU_BasicAugmentRGBSequence(data, nyu2_train, batch_size=batch_size, shape_rgb=shape_rgb, shape_depth=shape_depth)
    test_generator = NYU_BasicAugmentRGBSequence(data, nyu2_test, batch_size=batch_size, shape_rgb=shape_rgb, shape_depth=shape_depth)

    return train_generator, test_generator

class NYU_BasicAugmentRGBSequence(Sequence):
    def __init__(self, data, dataset, batch_size, shape_rgb, shape_depth, is_flip=False, is_addnoise=False, is_erase=False):
        self.data = data
        self.dataset = dataset
        self.policy = BasicPolicy( color_change_ratio=0.50, mirror_ratio=0.50, flip_ratio=0.0 if not is_flip else 0.2, 
                                    add_noise_peak=0 if not is_addnoise else 20, erase_ratio=-1.0 if not is_erase else 0.5)
        self.batch_size = batch_size
        self.shape_rgb = shape_rgb
        self.shape_depth = shape_depth
        self.maxDepth = 1000.0

        self.dataset = self.dataset.sample(frac = 1,random_state=0)

        self.N = len(self.dataset)

    def __len__(self):
        return int(np.ceil(self.N / float(self.batch_size)))

    def __getitem__(self, idx, is_apply_policy=True):
        batch_x, batch_y = np.zeros( self.shape_rgb ), np.zeros( self.shape_depth )

        # Augmentation of RGB images
        for i in range(batch_x.shape[0]):
            index = min((idx * self.batch_size) + i, self.N-1)

            sample = self.dataset.iloc[index]

            print(sample['rgb'])
            x = np.genfromtxt(sample['rgb'],delimiter=',').reshape(480,640,3,order='F')
            y = np.expand_dims(np.genfromtxt(sample['D'],delimiter=','),axis=2)
            
            
            # x = np.clip(np.asarray(Image.open(  )).reshape(480,640,3)/255,0,1)
            # y = np.clip(np.asarray(Image.open( BytesIO(self.data[sample[1]]) )).reshape(480,640,1)/255*self.maxDepth,0,self.maxDepth)
            # y = DepthNorm(y, maxDepth=self.maxDepth)

            print(x.shape)
            print(x)
            print(y.shape)
            batch_x[i] = nyu_resize(x, 480)
            batch_y[i] = nyu_resize(y, 240)

            if is_apply_policy: batch_x[i], batch_y[i] = self.policy(batch_x[i], batch_y[i])

            # DEBUG:
            #self.policy.debug_img(batch_x[i], np.clip(DepthNorm(batch_y[i])/maxDepth,0,1), idx, i)
        #exit()

        return batch_x, batch_y

# class NYU_BasicRGBSequence(Sequence):
#     def __init__(self, data, dataset, batch_size,shape_rgb, shape_depth):
#         self.data = data
#         self.dataset = dataset
#         self.batch_size = batch_size
#         self.N = len(self.dataset)
#         self.shape_rgb = shape_rgb
#         self.shape_depth = shape_depth
#         self.maxDepth = 1000.0

#     def __len__(self):
#         return int(np.ceil(self.N / float(self.batch_size)))

#     def __getitem__(self, idx):
#         batch_x, batch_y = np.zeros( self.shape_rgb ), np.zeros( self.shape_depth )
#         for i in range(self.batch_size):            
#             index = min((idx * self.batch_size) + i, self.N-1)

#             sample = self.dataset[index]

#             x = np.clip(np.asarray(Image.open( BytesIO(self.data[sample[0]]))).reshape(480,640,3)/255,0,1)
#             y = np.asarray(Image.open(BytesIO(self.data[sample[1]])), dtype=np.float32).reshape(480,640,1).copy().astype(float) / 10.0
#             y = DepthNorm(y, maxDepth=self.maxDepth)

#             batch_x[i] = nyu_resize(x, 480)
#             batch_y[i] = nyu_resize(y, 240)

#             # DEBUG:
#             #self.policy.debug_img(batch_x[i], np.clip(DepthNorm(batch_y[i])/maxDepth,0,1), idx, i)
#         #exit()

#         return batch_x, batch_y


if __name__ == '__main__':
    train_generator, test_generator = get_nyu_train_test_data(4)
    print(train_generator[0])
    print(test_generator[0])
