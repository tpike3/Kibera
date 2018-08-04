# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 15:07:04 2018

Tom Pike
CSS645
Kianda Slum Population During Riots
Visualization Module
"""


import shapefile as shp
import matplotlib.pyplot as plt


class Visualization(object): 

    def __init__(self): 
    
        #import shapefile
        self.sf = shp.Reader(".\\KIANDA_shapefile\\KIANDA_STRUCTURES\\Population_2\\kianda_structures_and_population_dataset.shp")
    
    
    def display(self):
        plt.figure(figsize=(15,15))
        for shape in self.sf.shapeRecords():
            
            # end index of each components of map
            l = shape.shape.parts
            
            len_l = len(l)  # how many parts of countries i.e. land and islands
            #print (len_l)
            x = [i[0] for i in shape.shape.points[:]] # list of latitude
            y = [i[1] for i in shape.shape.points[:]] # list of longitude
            l.append(len(x)) # ensure the closure of the last component
            for k in range(len_l):
                # draw each component of map.
                # l[k] to l[k + 1] is the range of points that make this component
                plt.plot(x[l[k]:l[k + 1]],y[l[k]:l[k + 1]], 'k-')
        
        # display
        plt.show()
