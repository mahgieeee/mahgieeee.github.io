"""
Created on Thu Oct 26 20:50:49 2017

@author: maggie
"""
from __future__ import print_function
from __future__ import division
from PIL import Image
import glob
import pickle
import scipy.misc
import numpy as np
from multiprocessing import Lock
from multiprocessing import Pool

def init(lock):
    global childs_lock
    childs_lock = lock

"""each pool worker gets original img data to reduce file size"""   
def reduce_images(image_path):
    childs_lock.acquire()
    img = Image.open(image_path)
    childs_lock.release()
    basewidth = 300
    percent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(percent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS) #ANTIALIAS reserves quality
    x_train = np.array(img)
    #x_train = np.array(img, dtype = np.uint8) #a numpy array with data type CV_8UC1
    #x_train = x_train[ : , : , 0] #slice out the color dimension
    print (x_train.shape)
    img.close()
    return x_train

#global storage variable for both main and pool of workers    
result_list = []

"""result(data) is called whenever process_images(path) returns a result
result_list is modified by main process not by pool of workers"""
def result(data):
    result_list.append(data)
    
    
if __name__ == '__main__':
    
    circle_path = "test_set/rectangle/"
    lock = Lock()
    p = Pool(processes=4, initargs = (lock, ), initializer = init)

    for image_path in glob.glob(circle_path + "*png"):
        p.apply_async(reduce_images, (image_path,), callback = result)
    
   
    p.close() # no more tasks
    p.join() #wrap up current tasks

    output = open ('test_rectangle.pkl', 'wb')
    for x in result_list:
        pickle.dump(x, output, -1)
    output.close()
   
    name = []
    num_files = 2000
    for i in range(num_files):
        name.append("test_set/rectangle1/rectangle" + str(i) + ".jpg")
    
    #save resized data to a folder
    with open('test_rectangle.pkl', 'rb') as pkl_file:
        data1 = [pickle.load(pkl_file) for i in range(num_files)]
    for i in range(num_files):
        scipy.misc.imsave(name[i], data1[i])
    
