#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy as np
import sys
from ..DBManager.DatabaseHandler import DatabaseHandler
from ..FacialRecognition.ModelBuilder import ModelBuilder
from keras.preprocessing import image
from keras.preprocessing.image import array_to_img
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
import cv2

class FacePredictor:
    def __init__(self, model, imageToPredict, dBFileName):
        self.model = model
        self.image = imageToPredict
        self.databaseHandler = DatabaseHandler(dBFileName)

    def predict(self, predictionScoreThreshold):
        # predImg = image.array_to_img(self.image).resize((64, 64))
        # testImage1 = np.expand_dims(predImg, axis = 0)
        # cv2.imwrite('/home/faten/Bureau/im_old.png', testImage1)
        # self.image = np.resize(self.image, (64, 64, 3))
        # print'=====>', type(self.image)
        # # sys.exit(0)
        # cv2.imwrite('/home/faten/Bureau/im.png', self.image)
        # cv2.imwrite('/home/faten/desktop/im.png', predImg)
        # cv2.imwrite('/home/faten/Bureau/im_old.png', self.image)
        predImg = image.array_to_img(self.image).resize((64, 64))
        # predImg.save('/home/faten/Bureau/im.png')

        testImage = np.expand_dims(predImg, axis = 0)
        model = ModelBuilder.loadModel(self.model)
        imageP = preprocess_input(testImage)

        scores = model.predict(imageP)[0]
        bestScoreIndex = np.argmax(scores)

        if scores[bestScoreIndex] > predictionScoreThreshold:
            data = self.databaseHandler.getDataByIndex(bestScoreIndex)
        else:
            data = None
        print 'Scores are ===>', scores
        print 'The estimated Person ===>', bestScoreIndex, scores[bestScoreIndex], data

        return data
