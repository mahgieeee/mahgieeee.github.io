"""
Created on Sun Nov 12 18:41:03 2017
Program loads pickle files and saves them as images in a folder 
@author: maggie
"""
from __future__ import print_function
import scipy.misc
from tensorflow.python.lib.io import file_io 
import joblib

def save_dataset(dataset, num, path):
    name = []
    for i in range(num):
        name.append(path + str(i) + ".jpg")    

    for x in range(num):
        print(name[x])
        scipy.misc.imsave(name[x], dataset[x])
        
        
if __name__ == '__main__':
    train_file = 'intersection_shapes_two.pkl'
    with file_io.FileIO(train_file , mode='r') as f:
        save = joblib.load(f)
        '''train_all = save['train_all']
        train_ctr = save['train_ctr']
        train_cts = save['train_cts']
        train_crs = save['train_crs']
        train_trs = save['train_trs']'''
        train_ct = save['train_ct']
        train_cr = save['train_cr']
        train_cs = save['train_cs']
        train_tr = save['train_tr']
        train_ts = save['train_ts']
        train_rs = save['train_rs']
        '''validation_all = save['validation_all']
        validation_train_ctr = save['validation_train_ctr']
        validation_train_cts = save['validation_train_cts']
        validation_train_crs = save['validation_train_crs']
        validation_train_trs = save['validation_train_trs']'''
        validation_train_ct = save['validation_train_ct']
        validation_train_cr = save['validation_train_cr']
        validation_train_cs = save['validation_train_cs']
        validation_train_tr = save['validation_train_tr']
        validation_train_ts = save['validation_train_ts']
        validation_train_rs = save['validation_train_rs']
        del save  # hint to help gc free up memory 
        
    
    '''save_dataset(train_all, 2000, 'intersection/all/all_')
    save_dataset(train_ctr, 2000, 'intersection/ctr/ctr_')    
    save_dataset(train_cts, 2000, 'intersection/cts/cts_')  
    save_dataset(train_crs, 2000, 'intersection/crs/crs_')  
    save_dataset(train_trs, 2000, 'intersection/trs/trs_')'''  
    save_dataset(train_ct, 2000, 'intersection/ct/ct_')  
    save_dataset(train_cr, 2000, 'intersection/cr/cr_') 
    save_dataset(train_cs, 2000, 'intersection/cs/cs_') 
    save_dataset(train_tr, 2000, 'intersection/tr/tr_') 
    save_dataset(train_ts, 2000, 'intersection/ts/ts_')
    save_dataset(train_rs, 2000, 'intersection/rs/rs_') 
    
    '''save_dataset(validation_all, 200, 'intersection/all/all_')
    save_dataset(validation_train_ctr, 200, 'validation_intersection/ctr/ctr_')    
    save_dataset(validation_train_cts, 200, 'validation_intersection/cts/cts_')  
    save_dataset(validation_train_crs, 200, 'validation_intersection/crs/crs_')  
    save_dataset(validation_train_trs, 200, 'validation_intersection/trs/trs_')'''  
    save_dataset(validation_train_ct, 200, 'validation_intersection/ct/ct_')  
    save_dataset(validation_train_cr, 200, 'validation_intersection/cr/cr_') 
    save_dataset(validation_train_cs, 200, 'validation_intersection/cs/cs_') 
    save_dataset(validation_train_tr, 200, 'validation_intersection/tr/tr_') 
    save_dataset(validation_train_ts, 200, 'validation_intersection/ts/ts_')
    save_dataset(validation_train_rs, 200, 'validation_intersection/rs/rs_') 

