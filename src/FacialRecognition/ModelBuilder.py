#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout, GaussianNoise
from keras.callbacks import ModelCheckpoint
from ..DBManager.DatabaseHandler import DatabaseHandler
from PIL import ImageFile
from keras.constraints import max_norm
from keras.constraints import unit_norm
# instantiate norm


class ModelBuilder:

    def __init__(self, nameModel):
        classifier = Sequential()
        #first model
        classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))
        classifier.add(MaxPooling2D(pool_size = (2, 2)))
        classifier.add(Dropout(0.4))

        classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
        classifier.add(MaxPooling2D(pool_size = (2, 2)))
        classifier.add(Dropout(0.4))
        classifier.add(Flatten())

        classifier.add(Dense(units = 128, activation = 'relu'))
        classifier.add(Dense(units = 2, activation = 'softmax'))


        #second model
        # classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))
        # classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))
        # classifier.add(MaxPooling2D(pool_size = (2, 2)))
        # classifier.add(Dropout(0.25))
        #
        # classifier.add(Conv2D(64, (3, 3), activation = 'relu'))
        # classifier.add(Conv2D(64, (3, 3), activation = 'relu'))
        # classifier.add(MaxPooling2D(pool_size = (2, 2)))
        # classifier.add(Dropout(0.25))
        # classifier.add(Flatten())
        #
        # classifier.add(Dense(units = 512, activation = 'relu'))
        # classifier.add(Dropout(0.5))
        # classifier.add(Dense(units = 2, activation = 'softmax'))

        self.classifier = classifier
        self.nameOfModel = nameModel

        ImageFile.LOAD_TRUNCATED_IMAGES = True

    def compileModel(self):
        self.classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

    def fitToDataset(self, trainingSetDir, testSetDir, nameDB):
        from keras.preprocessing.image import ImageDataGenerator

        train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

        test_datagen = ImageDataGenerator(rescale = 1./255,
                                    shear_range = 0.2,
                                    zoom_range = 0.2,
                                    horizontal_flip = True)

        training_set = train_datagen.flow_from_directory(trainingSetDir,
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

        keys1 = training_set.class_indices.keys()
        self.initializeDatabase(training_set.class_indices, keys1, nameDB)

        test_set = test_datagen.flow_from_directory(testSetDir,
                                            target_size = (64, 64),
                                            batch_size = 16,
                                            class_mode = 'categorical')
        filepath=self.nameOfModel
        checkpoint = ModelCheckpoint(str(filepath), monitor='val_acc', verbose=1, save_best_only=True, mode='max')
        callbacks_list = [checkpoint]

        self.classifier.fit_generator(training_set,
                         steps_per_epoch = 2400,
                         epochs = 25,
                         validation_data = test_set,
                         validation_steps = 400,
                         shuffle=True)
    def saveModel(self):
        self.classifier.save_weights(self.nameOfModel)

    def initializeDatabase(self, indexClasses, keys, nameDB):
        csvHandler = DatabaseHandler(nameDB).createFileStructure()

        for k in keys:
            valueOfClass =  indexClasses.get(k)
            csvHandler.saveOnto(valueOfClass, k)

    @staticmethod
    def loadModel(nameOfModel):
        model = Sequential([
            # Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'),
            # Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'),
            # MaxPooling2D(pool_size = (2, 2)),
            # Dropout(0.25),
            # Conv2D(64, (3, 3), activation = 'relu'),
            # Conv2D(64, (3, 3), activation = 'relu'),
            # MaxPooling2D(pool_size = (2, 2)),
            # Dropout(0.25),
            # Flatten(),
            # Dense(units = 512, activation = 'relu'),
            # Dropout(0.5),
            # # Dense(units = 128, activation = 'relu'),
            # Dense(units = 2, activation = 'softmax')
            Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'),
            MaxPooling2D(pool_size = (2, 2)),
            Dropout(0.4),
            Conv2D(32, (3, 3), activation = 'relu'),
            MaxPooling2D(pool_size = (2, 2)),
            Dropout(0.4),
            Flatten(),
            Dense(units = 128, activation = 'relu'),
            Dense(units = 2, activation = 'softmax')
        ])
        model.load_weights(nameOfModel)

        return model
