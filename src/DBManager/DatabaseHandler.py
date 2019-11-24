#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import csv
import os

class DatabaseHandler:
    data={}

    def __init__(self, dBFileName):
        self.dBFileName=dBFileName

    def createFileStructure(self):
        structure = ['index','cin','name','dateBirth', 'address', 'level']

        with open(self.dBFileName, mode='a') as csvFile:
            lineWriter = csv.writer(csvFile, delimiter=',')
            lineWriter.writerow([g for g in structure])

        return self

    def getDataByIndex(self, index):
        if not DatabaseHandler.data:
            with open(self.dBFileName, mode='r') as csvFile:
                lineReader = csv.reader(csvFile, delimiter=',')
                lineReader.next()

                for row in lineReader:
                    DatabaseHandler.data[int(row[0])] = {'cin':row[1],'name':row[2],'dateBirth':row[3],\
                    'address':row[4],'level':row[5]}

        return DatabaseHandler.data[index]

    def saveOnto(self, index, cin):
        with open(self.dBFileName, mode='a') as csvFile:
            lineWriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            lineWriter.writerow([index, cin])
