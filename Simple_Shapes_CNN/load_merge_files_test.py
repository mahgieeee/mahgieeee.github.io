from __future__ import print_function
import joblib
import numpy as np
from tempfile import mkdtemp
import os.path as path

'''returns individual list data info and y label data in numpy arrays''' 
def get_data(shape_temp_file, label_temp_file, dataset):
    # use memory mapping to store large datasets
    temp_filename = path.join(mkdtemp(), shape_temp_file)
    train_shape_dataset = np.memmap(temp_filename, 
                                    dtype = np.float16, 
                                    mode = 'w+', 
                                    shape = (300, 300, 3))
    temp_filename1 = path.join(mkdtemp(), label_temp_file)
    train_y_dataset = np.memmap(temp_filename1, 
                                dtype = np.float16, 
                                mode = 'w+', shape = (4))
    
    train_shape_dataset = [x[0] for x in dataset]
    # convert list back to np array for keras to process
    train_shape_dataset = np.array(train_shape_dataset)
    print ("in get_data function for dataset")
    print (train_shape_dataset.shape)
    train_y_dataset = [x[1] for x in dataset]
    train_y_dataset = np.array(train_y_dataset)
    print (train_y_dataset.shape)
    
    return train_shape_dataset, train_y_dataset

if __name__ == '__main__':
    pickle_file = 'data_shapes.pkl'
    np.random.seed(135)
    with open(str(pickle_file), 'rb') as f:
        # save = pickle.load(f)
        save = joblib.load(f)
        train_data = save['train_data']
        validation_data = save['validation_data']
        del save  # hint to help gc free up memory
        
    # shuffle the tuple (shape_info, y_label) dataset 
    np.random.seed(135)
    np.random.shuffle(train_data)

    # split list in half
    train_data_half = train_data[ :: 5]

    #validation_data_half = validation_data[ :: 3]
    
    train_shape_dataset, train_y_dataset = get_data('shapes.dat', 
                                                    'shapes_y.dat', 
                                                    train_data_half)
   
    validate_shape_dataset, validate_y_dataset = get_data('validate_shapes.dat', 
                                                          'validate_shapes_y.dat', 
                                                          validation_data)

    print ("in main: 1/third train shape", train_shape_dataset.shape)
    print ("in main: 1/third train y_label", train_y_dataset.shape)
    print ("in main: validate", validate_shape_dataset.shape)
    print ("in main: validate y_label", validate_y_dataset.shape)

    try:
        f = open(str('random_shapes_test.pkl'), 'wb')
        save = {'train_shape_dataset': train_shape_dataset,
                'train_y_dataset': train_y_dataset,
                'validate_shape_dataset': validate_shape_dataset,
                'validate_y_dataset': validate_y_dataset,
                }
        #pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        joblib.dump(save, f, compress = True)
        f.close()
    except Exception as e:
        print('Unable to save data to', str('random_shapes.pkl'), ':', e)
        raise
 
