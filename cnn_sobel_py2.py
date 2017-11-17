"""
Created on Sun Nov 12 18:41:03 2017
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
Nov 16: If offset is 50 or greater, the offset extends the original image when 
pasted on the background (ValueError: tile cannot extend outside image)
@author: maggie
"""
from __future__ import print_function
import cv2
from matplotlib import pyplot as plt
import numpy as np
from tensorflow.python.lib.io import file_io 
import joblib
import argparse
from PIL import Image
from datetime import datetime 
import scipy.misc

"""to run code locally:
   python cnn_sobel_py2.py --job-dir ./ --train-file cropped_random_shapes.pkl
"""
    
"""code to get boundaries of contour shapes and crops the images based on the 
location of the rectangular boundaries"""
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
    offset = 30
    crop_original_image = image_array[smallest_y + offset:largest_y + offset, 
                                      smallest_x + offset:largest_x + offset]
    #width, height = crop_original_image.shape[0], crop_original_image.shape[1]
    print (crop_original_image.shape)
     
    # resize the image using ratio 
    crop_image = Image.fromarray(np.uint8(crop_original_image))
    crop_width = 300
    percent = (crop_width / float(crop_image.size[0]))
    crop_height = int((float(crop_image.size[1]) * float(percent)))
    crop_image = crop_image.resize((crop_width, crop_height), Image.ANTIALIAS) #ANTIALIAS reserves quality
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

    '''plt.subplot(2,2,1),plt.imshow(image_array)
    plt.title('original image'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,2),plt.imshow(grayscale)
    plt.title('grayscale'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,3),plt.imshow(crop_original_image)
    plt.title('crop'), plt.xticks([]), plt.yticks([])'''
    return pasted_crop


def train_model(train_file = 'cropped_random_shapes.pkl',
                job_dir = './', 
                **args):
     # set the loggining path for ML Engine logging to storage bucket
    logs_path = job_dir + '/logs/' + datetime.now().isoformat()
    print('Using logs_path located at {}'.format(logs_path))

    with file_io.FileIO(train_file , mode='r') as f:
        # joblib loads compressed files consistenting of large datasets 
        # efficiently. 
        save = joblib.load(f)
        train_shape_dataset = save['train_shape_dataset']
        train_y_dataset = save['train_y_dataset']
        del save  # hint to help gc free up memory 
      
    name = []
    num_files = 200 
    for i in range(num_files):
        name.append("cropped_sobel/total_shapes/crop_" + str(i) + ".jpg")
        
    for x in range(num_files):
        scipy.misc.imsave(name[x], get_edges(train_shape_dataset[x]))

        
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

    
    
 
    


    
    

    
    
    
    
    
