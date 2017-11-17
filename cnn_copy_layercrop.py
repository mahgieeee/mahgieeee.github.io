#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 15:31:15 2017
This python 2 program will be implemented in the main cnn loader file, 
which will be incorporated with 2D cropping as a layer within keras. The cnn 
will be inputed with the original image, with cropping happening in between
@author: maggie
"""
from __future__ import print_function
from __future__ import division
import argparse
import cv2
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import Lambda
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.preprocessing.image import ImageDataGenerator
from datetime import datetime 
from PIL import Image
from tensorflow.python.lib.io import file_io 
import h5py
import joblib
import numpy as np
#import pickle

"""to run code locally:
   python cnn_copy_layercrop.py --job-dir ./ --train-file cropped_random_shapes.pkl 
"""
def get_edges(image_array): 
    
    # needed for cv2 to read the image in the proper color format
    original_img = cv2.cvtColor(np.array(image_array), cv2.COLOR_BGR2RGB)

    # requires the image to be in grayscale: 
    grayscale = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    
    # Gaussian to remove noise from 
    img = cv2.GaussianBlur(grayscale,(3,3),0)
    # Edge Detection Filter: use sobel algorithm to detect contours
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)  
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)  
    gradient_x = cv2.convertScaleAbs(sobelx)
    gradient_y = cv2.convertScaleAbs(sobely)
    # combine two sobel gradients
    gradient_t = cv2.addWeighted(gradient_x, 0.5, gradient_y, 0.5, 0)

    # Threshold filter
    # create threshold to separate edges from background
    # retval, thresh_gray = cv2.threshold(grayscale, thresh=127, 
                                         # maxval=255, type=cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(gradient_t, 
                                                cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(gradient_t, contours, 0, (0, 0, 255), 2)
     
    # with each contour, find 2 sets of coordinates to draw bounding rectangle
    # need to do list allocation here
    edge_list_x = []
    edge_list_y = []	
    for c in contours:
        x, y, width, height = cv2.boundingRect(c)
        # draw bounding rectangles around contours
        cv2.rectangle(grayscale, (x,y), (x+width, y+height), (0,255,0), 2) 
        edge_list_x.append(x)
        edge_list_y.append(y)
        edge_list_x.append(x+width)
        edge_list_y.append(y+height)
        
    smallest_x = min(edge_list_x)
    smallest_y = min (edge_list_y)
    largest_x = max(edge_list_x)
    largest_y = max(edge_list_y)
    
    # draws physical rectangle to be cropped
    # cv2.rectangle(grayscale, (smallest_x, smallest_y), 
    #             (largest_x, largest_y), (0,255,0), 2)
    offset = 15
    crop_original_image = image_array[smallest_y + offset:largest_y + offset, 
                                      smallest_x + offset:largest_x + offset]
    #width, height = crop_original_image.shape[0], crop_original_image.shape[1]
    #print (crop_original_image.shape)
     
    # resize the image using ratio 
    crop_image = Image.fromarray(np.uint8(crop_original_image))
    crop_width = 300
    percent = (crop_width / float(crop_image.size[0]))
    crop_height = int((float(crop_image.size[1]) * float(percent)))
    # ANTIALIAS reserves quality
    crop_image = crop_image.resize((crop_width, crop_height), Image.ANTIALIAS) 
    crop_image = np.array(crop_image, np.float32)
    
    # to deal with ambiguous images, just give it a single color 
    if (crop_width < 50 or crop_height < 50):
        crop_image[: , : , :] = [255, 255, 255] 
    
    # white background to create the same shapes (needed for keras generator)
    pasted_crop = Image.new("RGB", (300, 300), color = "white")
    # creating an image from a PIL array
    new_image = Image.fromarray(np.uint8(crop_image))
    pasted_crop.paste(new_image, (0, 0, crop_width, crop_height))
    # pasted_crop.show()
    
    # convert back to numpy array
    pasted_crop = np.array(pasted_crop, np.float32)

    return pasted_crop


def train_model(train_file = 'cropped_random_shapes.pkl',
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
        del save  # hint to help gc free up memory
        
    # Initialising the CNN by adding a simple sequential layer
    classifier = Sequential()
            
    # Step 1: 
    # Sequential layer consists of Convolution of type 3 by 3 convolutional 
    # window with 32 output filters(dimensionality of output space) for each 
    # input image uses relu layers to make layer less linear
    # the stride default is (1,1)
    classifier.add(Conv2D(32, (3, 3), input_shape = (300, 300, 3), activation = 'relu'))
    #classifier.add(Lambda(get_edges))
    # Step 2:  
    # Max Pooling downsamples the number pixels per neuron and create a max
    classifier.add(MaxPooling2D(pool_size = (2, 2)))

    # Adding a second convolutional layer, which is the same as the first one
    classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))


    # Step 3: Flattening the convolutional layers for input into a fully 
    # connected layer
    classifier.add(Flatten())
    
    # Step 4: 2 Layer Perceptron with Dropout
    classifier.add(Dense(units = 128, activation = 'relu'))
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
    classifier.compile(optimizer = 'adam', 
                       loss = 'categorical_crossentropy', 
                       metrics = ['accuracy'])

    # Part 2: 
    # Feeding CNN the input images and fitting the CNN 
    # CNN uses data augmentation configuration to prevent overfitting
    # datagen augmentation is for training data input
    datagen = ImageDataGenerator(rescale = 1./255,
                                 shear_range = 0.2,
                                 zoom_range = 0.2,
                                 horizontal_flip = True,
                                 preprocessing_function = get_edges) 
                         
    # compute quantities required for featurewise normalization
    datagen.fit(train_shape_dataset)
    # fits the model on batches with real-time data augmentation
    train_generator = datagen.flow(train_shape_dataset, 
                                   train_y_dataset, 
                                   batch_size = 32)
    classifier.fit_generator(train_generator, #train generator
                             steps_per_epoch = len(train_shape_dataset) / 32, 
                             epochs = 30)


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


