# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 11:39:32 2018

Add phenotypes which drive agent behavior


Tom Pike
CSS 645
"""

import numpy as np 

####################################################################
#
# Helper Functions--- PHYSICAL STATE
#
#####################################################################

def update_caldict(caldict, v): 
    
    if v["Age"] in caldict.keys(): 
        caldict[v["Age"]][0] += 1
    else: 
        caldict[v["Age"]] = [1, []]
    
    return caldict

def finish_caldict(caldict, reqdict, sd): 
    
    for k,v in reqdict.items(): 
        if k in caldict: 
            caldict[k][1] = np.random.normal(v, sd, caldict[k][0])
        
    return caldict

def calorie_array(agents): 
    
    #####################################################################
    #
    # Task: Create a normal distribution of calories requirents by age
    #
    #
    # Process: use numpy normal distribution function to create a normal distribution of the population 
    # based on USDA requirments for age and sednetary activity- used as Basal Metaboltic Rate
    # 
    #################################################################
    
    #USDA calories requirments table data based on age and moderate activity to create a baseline
    mal_reqs = {"0-4" : 1200, "5-9": 1400, "10-14": 1800, "15-18": 2400, "18-25": 2400, "25-50": 2400, "51+": 2200}
    #From sleep foundation 
    female_reqs = {"0-4" : 1000, "5-9": 1400, "10-14": 1600, "15-18": 1800, "18-25": 2000, "25-50": 1800, "51+": 1600}
    sleep_req = {"0-4": 13 , "5-9" : 12, "10-14": 10, "15-18": 8, "18-25": 8, "25-50": 8, "51+": 7}
    #from NAS
    mal_water =   {"0-4": 1.32 , "5-9" : 1.5, "10-14": 2.5, "15-18": 3.4, "18-25": 3.8, "25-50": 3.7, "51+": 3.5}
    female_water = {"0-4": 1.78 , "5-9" : 1.5, "10-14": 2.2, "15-18": 2.5, "18-25": 2.8, "25-50": 3.1, "51+": 3}
    
    cal_F = {}
    cal_M = {}
    water_M = {}
    water_F = {}
    sleep_all = {}
    
    #get number of males and females
    for v in agents.values():
        if v["Gender"] == "F": 
            cal_F = update_caldict(cal_F,v)
            water_F = update_caldict(water_F, v)
        else: 
            cal_M = update_caldict(cal_M, v)
            water_M = update_caldict(water_M,v)
        
        sleep_all = update_caldict(sleep_all,v)
    
    
    #create arrays for calories, water and sleep         
    #calories
    cal_F = finish_caldict(cal_F, female_reqs, 100)          
    cal_M = finish_caldict(cal_M, mal_reqs, 100)
    #water
    water_F= finish_caldict(water_F, female_water, 1)
    water_M = finish_caldict(water_M, mal_water, 1)
    #sleep
    sleep_all = finish_caldict(sleep_all, sleep_req, 1)
          
    return cal_F, cal_M, sleep_all, water_F, water_M
        

def p_input(k,v, req): 
    
    
    pos = np.random.randint(len(req[v["Age"]][1]))
    inp = req[v["Age"]][1][pos]
    req[v["Age"]][1] = np.delete(req[v["Age"]][1],[pos])
          
    return inp, req


    
    
    
    
########################################################################
#
# PHYSICAL STATE HELPER FUNCTION-----MAIN
#
#######################################################################
   

def add_physical_state(agents):
    
    ##########################################################
    #
    # Task: Add physical state calories, sleep and water
    #
    # Process: Standard deviation, per person and age
    #
    ############################################################    
    
    #create distributions of caloric requirments based on age and gender
    cal_req_F, cal_req_M, sleep_all, water_F, water_M = calorie_array(agents)
    
       
    for k,v in agents.items(): 
        
        #add calorie/hydration requirements to agents female
        if v["Gender"] == "F": 
            calorie, cal_req_F = p_input(k,v,cal_req_F)
            water, water_F = p_input(k,v,water_F)
            agents[k]["physical"] = {"caloric": [calorie,0], "hydration": [water,0]}
        
        #add calorie/hydration requirements male
        if v["Gender"] == "M": 
            calorie, cal_req_M = p_input(k,v,cal_req_M)
            water, water_M = p_input(k,v,water_M)
            agents[k]["physical"] = {"caloric": [calorie,0], "hydration": [water,0]}
            
        #add sleep requirements to agent
        sleep_r, sleep_all = p_input(k,v,sleep_all)
        agents[k]["physical"]["sleep"] = [sleep_r,0]
    
    del cal_req_F, cal_req_M, sleep_all, water_F, water_M
        
    return agents

###################################################################
#
# EmotionalState Helper Functions
#
##################################################################

'''
def fear_calc(agents): 
    
    fear_array, satisfaction_array = 
    
    for k,v in agents.items(): 
'''        





#####################################################################
#
# Emotional State Helper Function Main
#
######################################################################



def add_emotional_state(agents):
    
    for k in agents.keys(): 
        agents[k]["emotional"] = {"security": 1.0, "physical": 1.0, "social" : 0.5 }
        
    return agents


def add_behaviors(agents): 
    
    for k,v in agents.items(): 
        agents[k]["behavior"] = {"physical": ["eat", "hydrate", "sleep", "bathroom"],\
                                 "security": ["defend", "attack", "flee", "avoid"],
                                 "social": ["nurture", "engage-s", "engage-m", "engage-l", \
                                            "join", "reject", "learn"]}        
    return agents

################################################################
#
# Main Function 
#
###############################################################

def make_phenotypes(agents):
    
    print ("\nPhase V: Give Agents Physical Requirements.")     
    
    agents = add_physical_state(agents)
    agents = add_emotional_state(agents)
    agents = add_behaviors(agents)
    
    #print (agents[1262])
        
    return agents