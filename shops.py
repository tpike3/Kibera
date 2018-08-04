# -*- coding: utf-8 -*-
"""
Created on Fri May  4 13:19:10 2018



Tom Pike
CSS645
"""

import geopandas as gpd
import numpy as np

class Shops(object): 
    
    def __init__(self, row): 
        
        self.id = row[1]["STR_CODE"]
        self.center = row[1]['geometry'].centroid
        self.type = self.select_type(row)
        self.prices = self.make_prices(self.type)
        self.num_custs_per_4 = 0
        
        
        
        
    def select_type(self, row):
        '''
        Task: Select Shop type base don location
        
        Process: Assign one of 4 shop types based on structure code which are colocated
        '''
        
        if row[1]["STRUCTURE"] < 14: 
            return "24_cooked"
        elif row[1]["STRUCTURE"] >= 14 and row[1]["STRUCTURE"] < 25: 
            return  "24_raw"
        elif row[1]["STRUCTURE"] >= 25 and row[1]["STRUCTURE"] < 65: 
            return "raw"
        elif row[1]["STRUCTURE"] >= 65 and row[1]["STRUCTURE"] <= 100:
            return "cooked"
        elif row[1]["STRUCTURE"] > 100: 
            return "job_location" # job locations have cooked foods
        
    def make_prices(self, store_type): 
        
        '''
        Task: Give price array for shops
        
        Process: Set prices based on A Cost of the Diet Analysis in Kibera, Nairobi (Ndumi and Deptford 2013) and 
        fuel cost based on Food Insecurity in Urban Informal Settlements: A Case Study of Kibera, Nairobi (Abdulla 2011)
        '''
        
        food_prices = {"pack_2" : None, "pack_3" : None, "pack_4" : None}
        
        if store_type == "24_cooked" or store_type == "cooked" or store_type ==  "job_location":
            food_prices["pack_2"] = np.random.normal(4.74, .2) # #EO
                                                                  
            food_prices["pack_3"] = np.random.normal(7.99, .5) #MNUT
                                                                         # and oil +1.5 ksh for prep
                                                                       
            food_prices["pack_4"] = np.random.normal(12.08, 1) #LACON
                                                                         # and oil +1.5 ksh for prep
                                                                         
            
        if store_type == "24_raw" or store_type == "raw":
            food_prices["pack_2"] = np.random.normal(3.73, .2) # EO Diet
            food_prices["pack_3"] = np.random.normal(5.99, .5) # MNUT Diet 
                                                                       # (millet or wheat)
            food_prices["pack_4"] = np.random.normal(10.08, 1) #LACON Diet
            food_prices["fuel"] =   np.random.normal(.5, .1) #for kerosene                                                           # and oil
            
        return food_prices   
