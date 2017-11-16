#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 11:50:47 2017
Test cnn file on a small batch of data
@author: maggie
"""

from __future__ import print_function
from __future__ import division
import argparse
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.preprocessing.image import ImageDataGenerator
from datetime import datetime 
from tensorflow.python.lib.io import file_io 
import h5py
import joblib
#import pickle

def train_model(train_file = 'small_shapes.pkl', 
                job_dir = './', 
                **args):
    # set the loggining path for ML Engine logging to storage bucket
    logs_path = job_dir + '/logs/' + datetime.now().isoformat()
    print('Using logs_path located at {}'.format(logs_path))
    
    # need tensorflow to open file descriptor in order for google cloud to 
    # process it (instead of 'with open(loader, 'rb' as f:')
    with file_io.FileIO(train_file, mode='r') as f:
        # joblib loads compressed files consistenting of large datasets 
        # efficiently. 
        save = joblib.load(f)
        train_shape_dataset = save['train_shape_dataset']
        train_y_dataset = save['train_y_dataset']
        train_shape_halfdataset = save['train_shape_halfdataset']
        train_y_halfdataset = save['train_y_halfdataset']
        validate_shape_dataset = save['validate_shape_dataset']
        validate_y_dataset = save['validate_y_dataset']
        del save  # hint to help gc free up memory
        
    # Initialising the CNN by adding a simple sequential layer
    classifier = Sequential()

    # Step 1: 
    # Sequential layer consists of Convolution of type 3 by 3 convolutional 
    # window with 32 output filters(dimensionality of output space) for each 
    # input image uses reLU layers, which is a 
    # ''a nonlinear layer, network with relu is trained faster without creating 
    # a decrease in accuracy  @ adeshpande3.github.io''
    classifier.add(Conv2D(32, (3, 3), input_shape = (300, 300, 3), activation = 'relu'))

    # Step 2:  
    # Max Pooling downsamples the number pixels per neuron and create a max
    # number that describes those features in a pool_size of 2 by 2
    # change pool size from (2,2) to (8,8) to (4,4)
    classifier.add(MaxPooling2D(pool_size = (4, 4)))

    # Adding a second convolutional layer, which is the same as the first one
    classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
    # change pool size from (2,2) to (8,8)
    classifier.add(MaxPooling2D(pool_size = (4, 4)))
    # Dropout layers at the second convolutional layer before flattening 
    #classifier.add(Dropout(0.25)) #don't add dropout here to fix it? 11/11 Saturday

    # Step 3: Flattening the convolutional layers for input into a fully 
    # connected layer
    classifier.add(Flatten())
    
    # Step 4: 
    # Fully connected: Dense function is used to add a fully connected 
    # 3 layer perceptron at the end
    classifier.add(Dense(units = 128, activation = 'relu'))
    # dropout at the first layer perceptron
    classifier.add(Dropout(0.25))
    # adding second hidden layer - remove if accuracy decreases or loss increases
    classifier.add(Dense(units = 128, activation = 'relu'))
    classifier.add(Dropout(0.35))
    # softmax classifier as an activation from the last layer perceptron 
    # units represent number of output classes 
    # the output classes are triangle, rectangle, square, circle 
    classifier.add(Dense(units = 4, activation = 'softmax'))

    # Compiling the CNN: 
    # check if optimizer adam is good, categorical_crossentropy is for 
    # multi-class network, multilabel with intersection needs binary_crossentropy
    # and sigmoid activations
    # change from adam to rmsprop
    classifier.compile(optimizer = 'adam', 
                       loss = 'categorical_crossentropy', 
                       metrics = ['accuracy'])

    # Part 2: 
    # Feeding CNN the input images and fitting the CNN 
    # CNN uses data augmentation configuration to prevent overfitting
    # datagen augmentation is for training data input  
    datagen = ImageDataGenerator(featurewise_center = True,
                                 featurewise_std_normalization = True,
                                 rescale = 1./255,
                                 shear_range = 0.2,
                                 zoom_range = 0.2,
                                 horizontal_flip = True)
                                 preprocessing_function = get_edges(train_shape_dataset))
		                          
    # augmentation configuration for rescaling images used for validation 
    validate_datagen = ImageDataGenerator(rescale = 1./255)
    
    # the test set data augmentation only rescales the images 
    # is this enough to test the network correctly? if you want a more manual 
    # representation of fitting the input data use for loop
    validate_datagen.fit(validate_shape_dataset)
    validate_generator = datagen.flow(validate_shape_dataset, 
                                      validate_y_dataset, 
                                      batch_size = 32)
    
    # the code below fits the training data that is loaded by pickle file 
    # to prevent memory error, 1/2 of the number of data inputs are feed first
    # an epoch define the input being run once from 
    # the architecture of the cnn is:
    # 2DConv -> ReLU -> MaxPool -> 2DConv -> ReLU -> MaxPool -> Flatten() -> 
    # Fully connected 2-layer neural network 
    # 128 neurons for the first layer -> ReLU -> 128 for hidden layer -> ReLU 
    # -> 3 neurons for output layer -> softmax  
    
    # compute quantities required for featurewise normalization
    datagen.fit(train_shape_dataset)
    #early_stopping = EarlyStopping(monitor = 'val_loss', patience = 2)
    # fits the model on batches with real-time data augmentation
    train_generator = datagen.flow(train_shape_dataset, 
                                   train_y_dataset, 
                                   batch_size = 32)
    classifier.fit_generator(train_generator, #train generator
                             steps_per_epoch = len(train_shape_dataset) / 32, 
                             epochs = 20,
                             validation_data =  validate_generator,
                             validation_steps = 300)
    
    #early stopping prevent overfitting after the second half
    early_stopping = EarlyStopping(monitor = 'val_loss', patience = 2)
    # feed the same data generator the other half of the dataset
    datagen.fit(train_shape_halfdataset)
    train_generator_half = datagen.flow(train_shape_halfdataset, 
                                        train_y_halfdataset, 
                                        batch_size = 32)
    classifier.fit_generator(train_generator_half, 
                             steps_per_epoch = len(train_shape_halfdataset) / 32, 
                             epochs = 20,
                             callbacks = [early_stopping],
                             validation_data =  validate_generator,
                             validation_steps = 300)

	#evaluate the model 	               
    score = classifier.evaluate(validate_shape_dataset, 
                                validate_y_dataset, 
                                verbose = 0)
    print ("Test loss: ", score[0])
    print ("Test accuracy", score[1])

    classifier.save('model.h5')

    # Save the model to the Cloud Storage bucket's jobs directory
    with file_io.FileIO('model.h5', mode='r') as input_f:
        with file_io.FileIO(job_dir + '/model.h5', mode='w+') as output_f:
            output_f.write(input_f.read())


if __name__ == '__main__':
    # Parse the input arguments for common Cloud ML Engine options
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-file',
                        help='local path of pickle file')
    parser.add_argument('--job-dir', 
                        help='Cloud storage bucket to export the model')
    args = parser.parse_args()
    arguments = args.__dict__
    train_model(**arguments)

