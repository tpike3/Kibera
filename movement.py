# -*- coding: utf-8 -*-
"""
Created on Wed May  2 10:37:51 2018

Import GIS data to calculate movement

Tom Pike 
CSS645

"""

import geopandas as gpd
import pyproj
from shapely.ops import transform
import shapely
from functools import partial
import pandas as pd
import shops



class Movement(object):
    
    def __init__(self): 
        
        self.slum = self.convert(gpd.read_file("C:\\Users\\ymamo\\Kibera\\KIANDA_shapefile\\KIANDA_STRUCTURES\\Population_2\\kianda_structures_and_population_dataset.dbf"))
        self.water = self.convert(gpd.read_file("C:\\Users\\ymamo\\Kibera\\KIANDA_shapefile\\KIANDA_INFRA\\KIANDA_waterPT\\kibera_water_PT.shp"))
        self.centers = self.get_centers(self.slum)
        
    
    def convert(self, shape): 
                
        project = partial(pyproj.transform,
                    pyproj.Proj(init='epsg:4326'), # source coordinate system
                    pyproj.Proj(init='epsg:26913')) # destination coordinate system
        
        new_poly = []
        for poly in shape['geometry']: 
                new_poly.append(transform(project, poly))

        shape['geometry'] = pd.Series(new_poly)
        
        return shape

    
    
    def get_centers(self, df):
        
        project = partial(pyproj.transform,
                    pyproj.Proj(init='epsg:4326'), # source coordinate system
                    pyproj.Proj(init='epsg:26913'))
        
        centers = {}
        for struct in df.iterrows():
            centers[struct[1]["STR_CODE"]] = struct[1]["geometry"].centroid
            
        return centers
    
    
    def get_services(self):
        
        '''
        Task: Retrieve centroid of business locations in model
        
        Process: Uses geopandas distance (based on Shapley)
        
        '''
        
        slum_c = self.slum.loc[:,:] # makes new database instead of view of current one
        slum_c = slum_c[slum_c["BUSI_C"] >= 1] #eliminate non-service businesses
        
        business_dict = {}
        for row in slum_c.iterrows(): 
            business_dict[row[1]["STR_CODE"]] = row[1]['geometry'].centroid
    
        return business_dict #returns a panda series object which gives centroid to business polygon
    
    
    def get_water(self):
        
        water = self.water["geometry"]
        
        return water
    
    def shops(self): 
        
        shops_dict = {}
        
        slum_shop = self.slum.loc[:,:]
        slum_shop = slum_shop[slum_shop["BUSI_C"] >= 1]
        
        for row in slum_shop.iterrows():
            shop_agent = shops.Shops(row)
            shops_dict[shop_agent.id] = shop_agent
            #print (shop_agent.prices)   
        #stop
        return shops_dict
        
            
            
            
    
    
        
