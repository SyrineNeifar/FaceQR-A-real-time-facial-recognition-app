#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from src.FacialDetection.OpencvAbstraction import OpencvAbstraction
import configparser as cp
import os, sys
from os import listdir
from os.path import isfile
import cv2
from skimage import transform, color, exposure
from skimage.io import imsave
import numpy as np

config = cp.ConfigParser()
config.read('config.ini')

haarcascadeFileName = os.getcwd()+config.get('dir', 'haarcascade')+config.get('file', 'haarcascadeFileFace')
dataAugmentaionInputDir = os.getcwd() + config.get('dir', 'assets') + config.get('dir', 'dataAugmentaionInputDir')
dataAugmentaionOutputDir = os.getcwd() + config.get('dir', 'assets') + config.get('dir', 'preprocessing')

IMG_SIZE=64

def proprocess_img(img):
    min_side = min(img.shape[:-1])
    centre = img.shape[0] // 2, img.shape[1] // 2
    img = img[centre[0] - min_side // 2:centre[0] + min_side // 2,
              centre[1] - min_side // 2:centre[1] + min_side // 2]

    img = transform.resize(img, (IMG_SIZE, IMG_SIZE))
    return img

def proprocess_img_training(img):
    hsv=color.rgb2hsv(img)
    hsv[:,:,2]=exposure.equalize_hist(hsv[:,:,2])
    img = color.hsv2rgb(hsv)


    min_side = min(img.shape[:-1])
    centre = img.shape[0] // 2, img.shape[1] // 2
    img = img[centre[0] - min_side // 2:centre[0] + min_side // 2,
              centre[1] - min_side // 2:centre[1] + min_side // 2]
    #
    img = transform.resize(img, (IMG_SIZE, IMG_SIZE))
    # img=np.rollaxis(img, -1)
    return img


def execute(inputDir, outputDir):
    opencvAbstraction = OpencvAbstraction(haarcascadeFileName)

    for root, dirs, files in os.walk(inputDir, topdown=False):
        for name in files:
            filePath = os.path.join(root, name)
            print '>>> ',filePath

            image = cv2.imread(filePath)

            hasFaces, faces = opencvAbstraction.getFaces(image)

            if hasFaces:
                for (x, y, h, w) in faces:
                    imageFace = image[y:y + h, x: x + w]
                    fileOutputPath = filePath.replace(inputDir, outputDir)
                    fileOutputDir = os.path.dirname(fileOutputPath)
                    fileOutputPath = fileOutputPath.replace('.', '_' + str(x) + '_' + str(y) + '_' + str(h) + '_' + str(w) + '.')
                    print '<<< ', fileOutputPath

                    if not os.path.exists(fileOutputDir):
                        os.makedirs(fileOutputDir)

                    cv2.imwrite(fileOutputPath, proprocess_img(imageFace))


def execute_training(inputDir, outputDir):
    opencvAbstraction = OpencvAbstraction(haarcascadeFileName)

    for root, dirs, files in os.walk(inputDir, topdown=False):
        for name in files:
            filePath = os.path.join(root, name)
            print '>>> ',filePath

            image = cv2.imread(filePath)
            image = proprocess_img_training(image)
            cv2.imwrite("/home/faten/Bureau/prec.png", image)
            sys.exit(0)
            hasFaces, faces = opencvAbstraction.getFaces(image)
            if hasFaces:
                for (x, y, h, w) in faces:
                    imageFace = image[y:y + h, x: x + w]
                    fileOutputPath = filePath.replace(inputDir, outputDir)
                    fileOutputDir = os.path.dirname(fileOutputPath)
                    fileOutputPath = fileOutputPath.replace('.', '_' + str(x) + '_' + str(y) + '_' + str(h) + '_' + str(w) + '.')
                    print '<<< ', fileOutputPath

                    if not os.path.exists(fileOutputDir):
                        os.makedirs(fileOutputDir)

                    cv2.imwrite(fileOutputPath, imageFace)


execute_training(dataAugmentaionInputDir, dataAugmentaionOutputDir)
