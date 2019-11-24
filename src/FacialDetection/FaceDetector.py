#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#from OpencvAbstraction import OpencvAbstraction

class FaceDetector:

    def __init__(self, classifier, img):
         self.classifier = classifier
         self.image = img

    def detectFaces(self):
        from OpencvAbstraction import OpencvAbstraction

        gray = OpencvAbstraction.imageToGrayscaleTransform(self.image)
        faces = self.classifier.detectMultiScale(gray, 1.2, 5)

        if faces is ():
            return False, self.image

        return True, faces
