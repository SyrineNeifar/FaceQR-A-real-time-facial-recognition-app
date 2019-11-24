#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import cv2
from FaceDetector import FaceDetector
from AugmentedReality.ImageAugmentor import ImageAugmentor

class OpencvAbstraction:
    'Abstraction Layer of Opencv'
    faces = []
    hasFaces = False

    def __init__(self, haarcascadeFileName):
        self.cap = cv2.VideoCapture(0)
        self.faceClassifier = OpencvAbstraction.cascadeClassifier(haarcascadeFileName)



    def capture(self):

        s, img = self.cap.read()
        if s:
            pass

        self.image=img

    @staticmethod
    def cascadeClassifier(path):
        return cv2.CascadeClassifier(path)

    @staticmethod
    def imageToGrayscaleTransform(img):
        return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    @staticmethod
    def putRectangle(img, pt1, pt2, color, thickness=1, lineType=8, shift=0):
        cv2.rectangle(img, pt1, pt2, color, thickness, lineType, shift)

    @staticmethod
    def putLine(img, pt1, pt2, color, thickness=1, lineType=8, shift=0):
        cv2.line(img, pt1, pt2, color, thickness, lineType, shift)

    @staticmethod
    def putText(img, text, pt1, fontScale, color, thickness=1, lineType=8, bottomLeftOrigin=False) :
        cv2.putText(img, text, pt1, cv2.FONT_HERSHEY_DUPLEX, fontScale, color, thickness, lineType, bottomLeftOrigin)

    @staticmethod
    def getLineType():
        return cv2.LINE_AA

    @staticmethod
    def flip(img, flag):
        return cv2.flip(img,flag)

    def getFaces(self, image):
        faceDetector = FaceDetector(self.faceClassifier, image)

        return faceDetector.detectFaces()


    def show(self, frameTitle, frameIndex, dbName, modelName, detectionFrameCount, predictionScoreThreshold):
        if frameIndex % detectionFrameCount == 0:
            self.hasFaces, self.faces = self.getFaces(self.image)

        if self.hasFaces == True:
             ImageAugmentor(self.image, frameIndex, dbName, modelName) \
                .decorateFaces(self.faces, predictionScoreThreshold)
        else:
            ImageAugmentor.facesData = []

        # cv2.namedWindow(frameTitle,cv2.WINDOW_NORMAL)
        # cv2.resizeWindow(frameTitle, 640, 480)
        cv2.imshow(frameTitle, self.image)

    @staticmethod
    def destroyWindows():
        cv2.destroyAllWindows()

    def releaseCapture(self):
        self.cap.release()

    @staticmethod
    def waitQuitKey():
        return cv2.waitKey(1) & 0xFF == ord('q')
