#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
from multiprocessing import Pool
import numpy as geek
from ...FacialPrediction.FacePredictor import FacePredictor
from FaceDecorator import FaceDecorator

class ImageAugmentor:
    facesData = []

    def __init__(self, img, frameIndex, dBNameFile, modelNameFile):
        self.image = img
        self.frameIndex = frameIndex
        self.dBNameFile = dBNameFile
        self.modelNameFile = modelNameFile

    def decorateFaces(self, faces, predictionScoreThreshold):
        facesData = []

        for (x, y, w, h) in faces:
            data, dieFrameIndex = self.getfaceData(x, y, w, h, predictionScoreThreshold)

            facesData.append({'x': x + w / 2, 'y': y + h / 2, 'data': data, 'dieFrameIndex': dieFrameIndex})

            faceDecorator = FaceDecorator(self.image, x, y, w, h)
            faceDecorator.decorate(data, dieFrameIndex == self.frameIndex)

        ImageAugmentor.facesData = facesData

    def getfaceData(self, x, y, w, h, predictionScoreThreshold):
        for faceData in ImageAugmentor.facesData:
            if faceData['dieFrameIndex'] != self.frameIndex  \
                    and faceData['x'] > x and faceData['x'] < x + w \
                    and faceData['y'] > y and faceData['y'] < y + h:

                return faceData['data'], faceData['dieFrameIndex']
                
        facePredictor = FacePredictor(self.modelNameFile, self.image[y: y + h, x: x + w], self.dBNameFile)
        return facePredictor.predict(predictionScoreThreshold), self.frameIndex
