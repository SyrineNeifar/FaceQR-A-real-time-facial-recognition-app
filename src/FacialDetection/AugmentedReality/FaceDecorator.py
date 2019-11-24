#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
from multiprocessing import Pool
import numpy as geek

class FaceDecorator:
    COLOR_WHITE = (210, 210, 210)
    COLOR_GREEN = (0, 220, 0)
    COLOR_BLUE  = (194, 68, 72)
    COLOR_RED   = (68, 68, 255)

    def __init__(self, img, x, y, w, h):
        self.image = img
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def decorate(self, data, force):
        if force:
            color = FaceDecorator.COLOR_WHITE
        elif data is None:
            color = FaceDecorator.COLOR_RED
        else:
            color = FaceDecorator.COLOR_BLUE

        self.addRectangle(color)
        self.addAngles(color)
        self.addInformation(data, color)

    def addRectangle(self, color):
        from ..OpencvAbstraction import OpencvAbstraction

        OpencvAbstraction.putRectangle(self.image, (self.x, self.y), (self.x + self.w, self.y + self.h), color, 1)

    def addAngles(self, color):
        from ..OpencvAbstraction import OpencvAbstraction

        thickness = max(1, min(5, self.w / 50));

        OpencvAbstraction.putLine(self.image, (self.x + self.w * 3 / 4, self.y), (self.x + self.w, self.y), color, thickness)
        OpencvAbstraction.putLine(self.image, (self.x + self.w, self.y), (self.x + self.w, self.y + self.h / 4), color, thickness)

        OpencvAbstraction.putLine(self.image, (self.x + self.w, self.y + self.h * 3 / 4), (self.x + self.w, self.y + self.h), color, thickness)
        OpencvAbstraction.putLine(self.image, (self.x + self.w, self.y + self.h), (self.x + self.w * 3 / 4, self.y + self.h), color, thickness)

        OpencvAbstraction.putLine(self.image, (self.x + self.w / 4, self.y + self.h), (self.x, self.y + self.h), color, thickness)
        OpencvAbstraction.putLine(self.image, (self.x, self.y + self.h), (self.x, self.y + self.h * 3 / 4), color, thickness)

        OpencvAbstraction.putLine(self.image, (self.x, self.y + self.h / 4), (self.x, self.y), color, thickness)
        OpencvAbstraction.putLine(self.image, (self.x, self.y), (self.x + self.w / 4, self.y), color, thickness)

        wtdth = thickness * 4;

        OpencvAbstraction.putLine(self.image, (self.x + self.w / 2, self.y - wtdth), (self.x + self.w / 2, self.y + wtdth), color, 1)
        OpencvAbstraction.putLine(self.image, (self.x + self.w - wtdth, self.y + self.h / 2), (self.x + self.w + wtdth, self.y + self.h / 2), color, 1)
        OpencvAbstraction.putLine(self.image, (self.x + self.w / 2, self.y + self.h - wtdth), (self.x + self.w / 2, self.y + self.h + wtdth), color, 1)
        OpencvAbstraction.putLine(self.image, (self.x - wtdth, self.y + self.h / 2), (self.x + wtdth, self.y + self.h / 2), color, 1)

    def addInformation(self, data, color):
        from ..OpencvAbstraction import OpencvAbstraction

        thickness = min(2, self.w / 30);

        if data is None:
            OpencvAbstraction.putText(self.image, 'Unknown', (self.x + self.w + thickness * 4, self.y), 1, color, thickness)
        elif color == FaceDecorator.COLOR_BLUE:
            OpencvAbstraction.putText(self.image, data['name'], (self.x + self.w + thickness * 4, self.y), 1, color, thickness)
            OpencvAbstraction.putText(self.image, data['cin'], (self.x + self.w + thickness * 4, self.y+30), 1, color, thickness)
            OpencvAbstraction.putText(self.image, data['dateBirth'], (self.x + self.w + thickness * 4, self.y+60), 1, color, thickness)
            OpencvAbstraction.putText(self.image, data['address'], (self.x + self.w + thickness * 4, self.y+90), 1, color, thickness)
            OpencvAbstraction.putText(self.image, data['level'], (self.x + self.w + thickness * 4, self.y+120), 1, color, thickness)
