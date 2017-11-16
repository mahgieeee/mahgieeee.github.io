from __future__ import print_function
from PIL import Image
import glob
import pickle
import numpy as np
from multiprocessing import Lock
from multiprocessing import Pool
from keras.utils import to_categorical

"""to make lock and queue storage global to all child workers in the Pool"""
def init(lock):
    global childs_lock
    childs_lock = lock
    
def process_images(image_path, shape_path):
        shape_y = None
        if shape_path == "validation_set/circle/":
            shape_y = 0
        elif shape_path == "validation_set/rectangle/": 
            shape_y = 1
        elif shape_path == "validation_set/triangle/":
            shape_y = 2
	elif shape_path == "validation_set/square/":
            shape_y = 3
        
        ylabel = to_categorical(shape_y, num_classes = 4) 
        ylabel = np.reshape(ylabel, (4))
        print ("new shape", ylabel.shape)
        print (ylabel)
        childs_lock.acquire()
        img = Image.open(image_path)
        childs_lock.release()
        
        np_img = np.array(img, dtype = [('img_info', np.float16)])
        '''y_label = np.empty(None, dtype = [('y_class',np.int8)])
        y_label.fill(shape_y)'''
        # Add another dimension 1 image number for keras to process
        #np_img = np_img.reshape( (-1, ) + np_img.shape)  
        img.close()
        return np_img['img_info'], ylabel
    
#global storage variable for both main and pool of workers    
pickle_file = 'validate_square.pkl'
#create empty pickle_file first then append to file
output = open (pickle_file, 'wb')
output.close()

def result(data):
    output = open (pickle_file, 'ab')
    print ("in pickle file: " , pickle_file)
    pickle.dump(data, output, pickle.HIGHEST_PROTOCOL) 
    output.close()

if __name__ == '__main__':
        
    shape_path = "validation_set/square/" 
    lock = Lock()
    p = Pool(processes=4, initargs = (lock, ), initializer = init)
    #for shapes in shape_path:
    for image_path in glob.glob(shape_path + "*jpg"):
        p.apply_async(process_images, (image_path, shape_path), callback = result)
    p.close() # no more tasks
    p.join() #wrap up current tasks
    
    
    
    
