# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 15:07:42 2018

@author: ymamo
"""

import pandas as pd
import pickle


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
print ("starting")

filename =("C:\\Users\\ymamo\\Kibera\\Kianda Output.csv")

chunksize = 10 ** 4
print("read in")
for chunk in pd.read_csv(filename, chunksize=chunksize, low_memory = False):
    save_obj(chunk)


print ("complete")