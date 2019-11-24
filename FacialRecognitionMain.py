#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from src.FacialRecognition.ModelBuilder import ModelBuilder
import configparser as cp
import os

config = cp.ConfigParser()
config.read('config.ini')

modelFileName = os.getcwd()+config.get('dir', 'assets')+config.get('file', 'model')
trainingSetDir = os.getcwd()+config.get('dir', 'trainingSet')
testSetDir = os.getcwd()+config.get('dir', 'testSet')
dBFileName = os.getcwd()+config.get('dir', 'assets')+config.get('file', 'database')

modelBuilder = ModelBuilder(modelFileName)
modelBuilder.compileModel()
modelBuilder.fitToDataset(trainingSetDir, testSetDir, dBFileName)
modelBuilder.saveModel()
