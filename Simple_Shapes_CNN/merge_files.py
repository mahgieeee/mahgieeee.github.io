from __future__ import print_function
import pickle
import joblib
#import numpy as np
#from tempfile import mkdtemp
#import os.path as path

def load_train_or_test(files):    
    with open(files, 'rb') as f:
        try:
            print ("Opening files")
            print (files)
            while True:
                yield pickle.load(f) #python version 2.7
        except EOFError:
            pass
    
if __name__ == '__main__':
    
    #include (shape array,y_labels) as a tuple returned by the pickle
    circle_dataset = [item for item in load_train_or_test ("circle.pkl")]
    triangle_dataset = [item for item in load_train_or_test ("triangle.pkl")]
    rectangle_dataset = [item for item in load_train_or_test ("rectangle.pkl")]
    square_dataset = [item for item in load_train_or_test ("square.pkl")]

    #merge the individual shape data into one train_data
    train_data = circle_dataset + triangle_dataset + rectangle_dataset + square_dataset
    
    validation_circle_dataset = [item for item in load_train_or_test ("validate_circle.pkl")]
    validation_triangle_dataset = [item for item in load_train_or_test ("validate_triangle.pkl")]
    validation_rectangle_dataset = [item for item in load_train_or_test ("validate_rectangle.pkl")]
    validation_square_dataset = [item for item in load_train_or_test ("validate_square.pkl")]

    validation_data = validation_circle_dataset + validation_triangle_dataset + validation_rectangle_dataset + validation_square_dataset

    pickle_file = 'shape_data.pkl'
    try:
        f = open(pickle_file, 'wb')
        save = {#'train_shape_dataset': train_shape_dataset,
                'train_data': train_data,
                'validation_data': validation_data,
                }
        #pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        joblib.dump(save, f, compress = True)
        f.close()
    except Exception as e:
        print('Unable to save data to', pickle_file, ':', e)
        raise
   
    
 
