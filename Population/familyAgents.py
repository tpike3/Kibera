# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:51:21 2018

@author: ymamo
"""

import geopandas as gpd
import math
from operator import itemgetter



#global count 

#########################################
#
# HELPER FUNCTION
#
########################################

def calc_distance(origin, dest):
    
    '''
    
    Task: Calculate distance from agent house to every shop or water point
    
    Process: use centroid method to go from center of house to center of shop; 
    create list with identification number and distance to store
    
    '''
    
    '''
    global count 
    
    count += 1
    
    if count%1000 == 0: 
        print ("Calculating distances to shops for families")
        print ("On family: ", count)
    '''  
    
    distances = []
    for v in dest:
              
        
        #distances.append(float(origin.distance(x))
        try: 
            distances.append((v.id, float(origin.distance(v.center))))
        except: 
            print ("ERROR IN shp file")
        
        distances.sort(key=itemgetter(1))
    
    return distances


def calc_distance_w(origin, water): 
    
    '''
    
    Task: Calculate disitance ofrm agent house to all water points if they do nothave water
    
    Process: centroid house to centroid house use shapey distance method
    
    '''
        
    '''
    global count 
    
    count += 1
    
    if count%1000 == 0: 
        print ("Calculating distances to water for families")
        print ("On family: ", count)
    '''    
    
    distances = []
    for k,v in water.items():
                
        distances.append((k, float(origin.distance(v))))
        
    distances.sort(key=itemgetter(1))
    
    return distances



def get_water(house,water, gis): 
    
    origin = gis.centers[house]
    
    water_prox = calc_distance_w(origin, water)
    
    return water_prox



def get_business(house, services, gis): 
    
    '''
    Task: Create an attribute which lists businesses in order of distance
    
    Process: Use shp file to determine distance (lat/long)  and then law of cosines to convert 
    to meters
    
    '''
    #og = gis.get_house(house)     
    #get centroid of family structure
    origin = gis.centers[house]
    
    #get a list of distances in meter
    
    bus_prox = calc_distance(origin, services)
    
    return bus_prox


def add_family(families,k,v):
    
    families[v['Family']]["Tribe"] = v["Tribe"]
    families[v["Family"]]["Requirements"]["Caloric"][0] += v["physical"]["caloric"][0]
    families[v["Family"]]["Requirements"]["Hydration"][0] += v["physical"]["hydration"][0]

    if v["Age"] == "0-4": #future iteration or v["Age"] == "5-9":
        families[v["Family"]]["Requirements"]["Nurturing"] += 1
    if v["Age"] == "10-14":
        #print (families[v["Family"]]["Resources"])
        families[v["Family"]]["Resources"]["Poss Child Labor"] += 1
    families[v['Family']]["Members"][k] = {"Age": v["Age"], "Employment": v["Employment"], "Gender" : v["Gender"], \
                                            "Sleep": [v["physical"]["sleep"][0],  v["physical"]["sleep"][0], v["physical"]["sleep"][0]/17], \
                                            "Caloric": [v["physical"]["caloric"][0], v["physical"]["caloric"][0]- (v["physical"]["caloric"][0]/3), v["physical"]["caloric"][0]/24], \
                                            "Hydration": [v["physical"]["hydration"][0], v["physical"]["hydration"][0]], \
                                            "Emotion" : v["emotional"], "Bias" : 2.0, "Meal" : False, "Work": ""} 
    families[v['Family']]["Actions"] = {"Sleep": 0, "Drink": 0, "Eat": 0, "Partial Eat": 0, "Work": 0, "Look for Work": 0, "Steal": 0, \
                                        "variety_4" : 0, "variety_3" : 0, "variety_2" : 0, "Cook": 0, "Social" : 0, "Buy Food" : 0,\
                                        "Skip Meal": 0, "Buy Fuel": 0, "Educate":0, "Nurture": 0, "Needs Met":0, "child_labor" : 0, \
                                        "Child Danger": 0, "Food Cost":0, "Steal daily" : 0} 
    
    families[v["Family"]]["Resources"]["Wealth"] = 0
    
    
    
    '''
   
    
    Provide initial value of water on hand for those who do not have any
    
    '''
    if families[v["Family"]]["Resources"]["Water"] == None: 
        families[v["Family"]]["Resources"]["Water2"] = 0
    
    families[v["Family"]]["Resources"]["Food_cooked"] += v["physical"]["caloric"][0]/3
    
    if "Water2" in families[v["Family"]]["Resources"].keys(): 
        families[v["Family"]]["Resources"]["Water2"] += v["physical"]["hydration"][0]/3
       
    return families
    

def shop_breakdown(shops):
    
    shops_type = {}
    
    for v in shops.values(): 
        if v.type in shops_type: 
            shops_type[v.type].append(v)
        else: 
            shops_type[v.type] = [v]
    
    return shops_type
            


##########################################
#
# MAIN FUNCTION 
#
##########################################


def make_families(agents,gis, shops):
    
    print ("")
    #global count 
    #count = 0
    
    print ("Phase VI: \n")
    print ("Calculating distances to shops and water points.")
    
    
    shop_types = shop_breakdown(shops)
    
    services = gis.get_services() #returns dictionary k is structure, value is centroid
    water = gis.get_water()

    
    families = {}
    
    for k,v in agents.items(): 
        
        if v["Family"] not in families: 
            
            families[v["Family"]] = {"Requirements" : {"Caloric" : [0,0], "Hydration": [0,0], "Nurturing" : 0, "Rent": v["RENT"]}, \
                                    "Members" : {}, 
                                    "Resources" : {"Wealth" : 0, "Food_cooked": 0, "Food_uncooked": 0, "Electricity" : v["Electricity"],\
                                                   "House": v["House"], "Water": v["Water"], "Toilet": v["Toilet"], "Poss Child Labor" : 0}, \
                                     "B_cooked": get_business(v["House"], shop_types["cooked"], gis), \
                                     "B_raw": get_business(v["House"], shop_types["raw"], gis), \
                                     "B_jobs": get_business(v["House"], shop_types["job_location"], gis),\
                                     "B_24_cooked": get_business(v["House"], shop_types["24_cooked"], gis),\
                                     "B_24_raw": get_business(v["House"], shop_types["24_raw"], gis)}
            
            if v["Water"] == None: 
                families[v["Family"]]["Water_points"] = get_water(v["House"], water, gis)
            else: 
                #print (v["Water"])
                families[v["Family"]]["Water_points"] = "NA"
                
            families = add_family(families, k, v)
            
        else: 
            families = add_family(families, k, v)
            
    #del services
    #del water
    #print ("\n", families[456])
    
    print ("")
            
    return families, services, water