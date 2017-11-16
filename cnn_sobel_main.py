"""
Created on Sun Nov 12 18:41:03 2017
Program finds contours and creates a rectangular boundary around it
This python 2 program will be implemented in the cnn loader file  
testing nested functions incorporated with command line because there is a segmentation
fault from the pickle load.  
@author: maggie
"""
from __future__ import print_function
import glob
import cv2
from matplotlib import pyplot as plt
import scipy.misc
import numpy as np
from tensorflow.python.lib.io import file_io 
import joblib
import argparse

"""to run code locally:
   python cnn_sobel_py2.py --job-dir ./ --train-file cropped_random_shapes.pkl 
"""
    
"""code to get boundaries of contour shapes and crops the images based on the 
location of the rectangular boundaries"""
def get_edges(image_array):    
    #change from np.float16 to np.float32 in pickletestcats file
    #new_image_converted = image_array.astype(np.float32)
    # needed for cv2 to read the image in the proper color format
    original_img = cv2.cvtColor(np.array(image_array), cv2.COLOR_BGR2RGB)

    # requires the image to be in grayscale: 
    # convert copy of original image array to grayscale
    grayscale = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    
    # Gaussian to remove noise from 
    img = cv2.GaussianBlur(grayscale,(3,3),0)
    # Edge Detection Filter: use sobel algorithm to detect edges
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)  
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)  
    gradient_x = cv2.convertScaleAbs(sobelx)
    gradient_y = cv2.convertScaleAbs(sobely)
    #combine two sobel gradients
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
    
    offset = 5 
    # draws physical rectangle to be cropped
    # cv2.rectangle(grayscale, (smallest_x, smallest_y), 
    #             (largest_x, largest_y), (0,255,0), 2)
    # use this function to crop on original image in keras 2Dcropping 
    # (extra layer between CNN layers) 
    crop_original_image = image_array[smallest_y + offset:largest_y + offset, 
                                      smallest_x + offset:largest_x + offset]
    print ("Shape of cropped image: " , crop_original_image.shape)
    
    '''plt.subplot(2,2,1),plt.imshow(image_array)
    plt.title('original image'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,2),plt.imshow(grayscale)
    plt.title('grayscale'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,3),plt.imshow(crop_original_image)
    plt.title('crop'), plt.xticks([]), plt.yticks([])'''
    
    return crop_original_image
    #return image_array

if __name__ == '__main__':
    train_file = 'single_cropped_circle.pkl'
    with file_io.FileIO(train_file , mode='r') as f:
        # joblib loads compressed files consistenting of large datasets 
        # efficiently. 
        save = joblib.load(f)
        train_shape_dataset = save['circle_dataset']
        #train_y_dataset = save['train_y_dataset']
        del save  # hint to help gc free up memory 
        
    print (train_shape_dataset[0].shape)
    get_edges(train_shape_dataset[0])
    
    name = []
    num_files = 10
    for i in range(num_files):
        name.append("cropped_sobel/crop" + str(i) + ".jpg")
        
    for x in range(10):
        scipy.misc.imsave(name[x], get_edges(train_shape_dataset[x]))
        
    #plt.imshow(get_edges(train_shape_dataset[100]))

    
    
 
    


    
    

    
    
    
    
    
