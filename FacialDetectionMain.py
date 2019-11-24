#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from src.FacialDetection.OpencvAbstraction import OpencvAbstraction
import configparser as cp
import os

config = cp.ConfigParser()
config.read('config.ini')

haarcascadeFileName = os.getcwd()+config.get('dir', 'haarcascade')+config.get('file', 'haarcascadeFileFace')
dBFileName = os.getcwd()+config.get('dir', 'assets')+config.get('file', 'database')
modelFileName = os.getcwd()+config.get('dir', 'assets')+config.get('file', 'model')
predictionFrameCount = int(config.get('params', 'predictionFrameCount'))
predictionScoreThreshold = float(config.get('params', 'predictionScoreThreshold'))
detectionFrameCount = int(config.get('params', 'detectionFrameCount'))

capture = OpencvAbstraction(haarcascadeFileName)
frameIndex = 0;

while True:
    capture.capture()
    capture.show('SmartGlass Application', frameIndex, \
        dBFileName, modelFileName, detectionFrameCount, predictionScoreThreshold)

    frameIndex = (frameIndex + 1) % predictionFrameCount

    if OpencvAbstraction.waitQuitKey():
        break

capture.releaseCapture()
OpencvAbstraction.destroyWindows()
