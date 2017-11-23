"""
Created on Mon Nov 13 11:50:47 2017
Program finds contours by using the sobel algorithm. After finding
the countours, rectangular boundaries are drawn around it. The 
locations of the rectangles are in (x,y) coordinates where the cropped
version will be from the top left corner (smallest_x, smallest_y)
and the bottom right opposite corner (largest_x, largest y). get_edges
creates a copy of the image that needs to be in grayscale for the 
sobel algorithm. After the boundary is found, cropping of the original
image will be done through array slicing. This python 2 program will be 
implemented in the main cnn loader file, which will be incorporated with 
the cropping of images as a function. The cnn will see the images cropped 
and will not see the original image.  
@author: maggie
"""
from __future__ import print_function
from __future__ import division
import argparse
import cv2
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.preprocessing.image import ImageDataGenerator
from datetime import datetime 
from PIL import Image
from tensorflow.python.lib.io import file_io 
import h5py
import joblib
import numpy as np
#import pickle

"""to run code locally:
   python cnn_copy_sobel.py --job-dir ./ --train-file cropped_random_shapes.pkl 
"""
    
"""code to get boundaries of contour shapes and crops the images based on the 
location of the rectangular boundaries. The cropped image has to be within the 
same shape as the original image (300, 300, 3) - pasted the cropped image.  
Convolutional 2D layers will need to deal with the white background either
by changing the stride in the convolution or making a function for stride 
to stop at the end pixels of the cropped shape"""
def get_edges(image_array):    
    # needed for cv2 to read the image in the proper color format
    new_image_converted = image_array.astype(np.float32)
    original_img = cv2.cvtColor(new_image_converted, cv2.COLOR_BGR2RGB)

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
    offset = 0
    crop_original_image = image_array[smallest_y + offset:largest_y + offset, 
                                      smallest_x + offset:largest_x + offset]
    width, height = crop_original_image.shape[0], crop_original_image.shape[1]
    print (crop_original_image.shape)
     
    # resize the image using ratio 
    #crop_image = Image.fromarray(np.uint8(crop_original_image))
    #crop_width = 300
    #percent = (crop_width / float(crop_image.size[0]))
    #crop_height = int((float(crop_image.size[1]) * float(percent)))
    #crop_image = crop_image.resize((crop_width, crop_height), Image.ANTIALIAS) #ANTIALIAS reserves quality
    #crop_image = np.array(crop_image, np.float32)
    
    # to deal with ambiguous images, just give it a single color 
    if (width < 50 or height < 50):
        crop_original_image[: , : , :] = [255, 255, 255] 
    
    # white background to create the same shapes (needed for keras generator)
    pasted_crop = Image.new("RGB", (300, 300), color = "white")
    # creating an image from a PIL numpy array
    new_image = Image.fromarray(np.uint8(crop_original_image))
    pasted_crop.paste(new_image, (0, 0, height, width))
    
    # convert back to numpy array
    pasted_crop = np.array(pasted_crop, np.float16)
    
    return pasted_crop

def train_model(train_file = 'gs://cnninput_dataset/data/random_shapes.pkl',
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
        train_shape_halfdataset1 = save['train_shape_halfdataset1']
        train_y_halfdataset1 = save['train_y_halfdataset1']
        validate_shape_dataset = save['validate_shape_dataset']
        validate_y_dataset = save['validate_y_dataset']
        del save  # hint to help gc free up memory
        
    # Initialising the CNN by adding a simple sequential layer
    classifier = Sequential()

    # Step 1: 
    # Sequential layer consists of Convolution of type 3 by 3 convolutional 
    # window with 32 output filters(dimensionality of output space) for each 
    # input image uses relu layers to make layer less linear
    # the stride default is (1,1)
    classifier.add(Conv2D(32, (3, 3), input_shape = (300, 300, 3), activation = 'relu'))

    # Step 2:  
    # Max Pooling downsamples the number pixels per neuron and create a max
    # number that describes those features in a pool_size of 4 by 4
    classifier.add(MaxPooling2D(pool_size = (4, 4)))

    # Adding a second convolutional layer, which is the same as the first one
    classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
    # change pool size from (2,2) to (8,8)
    classifier.add(MaxPooling2D(pool_size = (4, 4)))


    # Step 3: Flattening the convolutional layers for input into a fully 
    # connected layer
    classifier.add(Flatten())
    
    # Step 4: 
    # Fully connected: Dense function is used to add a fully connected 
    # 3 layer perceptron at the end
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
    datagen = ImageDataGenerator(#featurewise_center = True,
                                 #featurewise_std_normalization = True,
                                 rescale = 1./255,
                                 shear_range = 0.2,
                                 zoom_range = 0.2,
                                 horizontal_flip = True)
                                 #preprocessing_function = get_edges) 
                         
    # augmentation configuration for rescaling images used for validation 
    validate_datagen = ImageDataGenerator(rescale = 1./255)
                                          #preprocessing_function = get_edges)
    
    # the test set data augmentation only rescales the images 
    # is this enough to test the network correctly? if you want a more manual 
    # representation of fitting the input data use for loop
    validate_datagen.fit(validate_shape_dataset)
    validate_generator = validate_datagen.flow(validate_shape_dataset, 
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
    
    # early stopping prevent overfitting after the second half
    early_stopping = EarlyStopping(monitor = 'val_loss', patience = 2)
    
    # compute quantities required for featurewise normalization
    datagen.fit(train_shape_dataset)
    # fits the model on batches with real-time data augmentation
    train_generator = datagen.flow(train_shape_dataset, 
                                   train_y_dataset, 
                                   batch_size = 32)
    classifier.fit_generator(train_generator, 
                             steps_per_epoch = len(train_shape_dataset) / 32, 
                             epochs = 30,
                             callbacks = [early_stopping],
                             validation_data =  validate_generator,
                             validation_steps = 300)
    

    # feed the same data generator the other half of the dataset
    datagen.fit(train_shape_halfdataset)
    train_generator_half = datagen.flow(train_shape_halfdataset, 
                                        train_y_halfdataset, 
                                        batch_size = 32)
    classifier.fit_generator(train_generator_half, 
                             steps_per_epoch = len(train_shape_halfdataset) / 32, 
                             epochs = 30,
                             callbacks = [early_stopping],
                             validation_data =  validate_generator,
                             validation_steps = 300)

    datagen.fit(train_shape_halfdataset1)
    train_generator_third = datagen.flow(train_shape_halfdataset1, 
                                        train_y_halfdataset1, 
                                        batch_size = 32)

    classifier.fit_generator(train_generator_third, 
                             steps_per_epoch = len(train_shape_halfdataset1) / 32, 
                             epochs = 30,
                             callbacks = [early_stopping],
                             validation_data =  validate_generator,
                             validation_steps = 300)
    # evaluate the model 	               
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


