import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import keras
import numpy as np
import sys
import os
import cv2
import scipy

from PIL import Image
from os import listdir
from os.path import isfile
from keras import backend as K
from scipy import misc, ndimage
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

dirInitialImages='/home/faten/Bureau/dataset/test/'
dirAugmentedImages=dirInitialImages+'augmented/'


def getlistFiles(filePath, fileExtension):
    listF=[]
    for i in range(10):
        listF.append(filePath+str(i)+fileExtension)
    return listF

# def plots(ims, figsize=(12,6), rows=1, interp=False, titles=None):
#     if type(ims[0]) is np.ndarray:
#         ims = np.array(ims).astype(np.uint8)
#         if (ims.shape[-1] != 3):
#             ims = ims.transpose((0,2,3,1))
#             print '*****', ims.shape()
#     f = plt.figure(figsize=figsize)
#     cols = len(ims)//rows if len(ims) % 2 == 0 else len(ims)//rows + 1
#     # scipy.misc.toimage(ims[1], cmin=0, cmax=255).save('HI.png')
#
#     return ims
    # for i in range(len(ims)):
        # sp = f.add_subplot(rows, cols, i+1)
        # sp.axis('Off')
        # if titles is not None:
        #     sp.set_title(titles[i], fontsize=16)
        # plt.imshow(ims[i], interpolation=None if interp else 'none')

gen=ImageDataGenerator(rotation_range=10, width_shift_range=0.1,\
                        height_shift_range=0.1, shear_range=0.15,zoom_range=0.1, \
                        channel_shift_range=10, horizontal_flip=True)


for imageC in listdir(dirInitialImages):
    imagePath = dirInitialImages + imageC
    if isfile(imagePath):
        imageM = np.expand_dims(plt.imread(imagePath),0) #obtain image

        # from PIL import Image
        # width, height = len(imageM[0]), len(imageM)
        #data = sum(imageM, []) # ugly hack to flatten the image
        # im = Image.new('RGB', (width, height))
        # im.putdata(imageM.flatten())
        # im.save('Bessem.png')
        # sys.exit(0)

        aug_iter = gen.flow(imageM)
        aug_images = [next(aug_iter)[0].astype(np.uint8) for i in range(10)]
        # aug_images1 = np.array(aug_images)

        saveImgPath=dirAugmentedImages+imageC
        nameImgWithoutExtension=os.path.splitext(saveImgPath)[0]
        nameImgExtension=os.path.splitext(saveImgPath)[1]
        file_names = getlistFiles(nameImgWithoutExtension, nameImgExtension)

        # np.save(dirAugmentedImages+imageC, aug_images1)
        # aug_images1 = np.load(dirAugmentedImages+imageC)
        # aug_images = plots(aug_images, figsize=(20,7), rows=2)

        for i in range(len(aug_images)):
            print i
            mpimg.imsave(file_names[i], aug_images[i])
        #     # plt.imshow(aug_images[i])
        #     saveImgPath=dirAugmentedImages+imageC
        #     nameImgWithoutExtension=os.path.splitext(saveImgPath)[0]
        #     nameImgExtension=os.path.splitext(saveImgPath)[1]

            # import cv2
            # cv2.imwrite(nameImgWithoutExtension+str(i)+nameImgExtension, aug_images[i])
            # plt.imsave(nameImgWithoutExtension+str(i)+nameImgExtension, aug_images[i])
            # from keras.preprocessing.image import array_to_img
            # predImg = image.array_to_img(aug_images[i])
            # print '=======>', type(aug_images)
            # print '=======>', type(aug_images[i])
            # print '=======>', type(predImg)
            # testImage = np.expand_dims(predImg, axis = 0)
            # print '=======>', type(testImage)

            # from PIL import Image
            # im = Image.fromarray(aug_images[i]) #make sure you have a uint8 from 0 to 255 array.
            # im.save(nameImgWithoutExtension+str(i)+nameImgExtension)

            # cv2.imwrite(nameImgWithoutExtension+str(i)+nameImgExtension, aug_images[i])
            # scipy.misc.toimage(aug_images[i], cmin=0, cmax=255).save(nameImgWithoutExtension+str(i)+nameImgExtension)
            # f.savefig(nameImgWithoutExtension+str(i)+nameImgExtension)
#image_path = '/home/faten/Bureau/dataset/Bessem/IMG_4042.JPG'
#plt.imshow(image[0])

#generate batches of augmented images from this image
#get 10 samples of augmented images
