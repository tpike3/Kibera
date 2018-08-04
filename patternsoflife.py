# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 14:47:33 2018
Create Decision Trees for agents based on maslow heirarchy of needs


Tom Pike
CSS 645
"""

import math
import actions


def check_physical(members):
    
    #######################################################
    #   #Task: Calcuate Current Sleep needs
    #
    #Process: use logistic function with varying slopes based on physical need
    #
    ######################################################   
    
    family_needs = {} 
    
    for k,v in members.items(): 
        family_needs[k] = {}
        try: 
            family_needs[k]["Sleep"] = 1/(1+math.exp((v["Sleep"][1]/v["Sleep"][0])))
        except: 
            family_needs[k]["Sleep"] = 0
        try: 
            family_needs[k]["Calories"] = 1/(1+math.exp(0.5*(v["Caloric"][1]/v["Caloric"][0])))
        except:
            family_needs[k]["Calories"] = 0
        family_needs[k]["Hydration"] = 1/(1+math.exp((v["Hydration"][1]/v["Hydration"][0])))
        family_needs[k]["Meal"] = v["Meal"]
        
    return family_needs


def check_status(agent): 
    
    '''
    
    Task: Check status of various needs
    
    Process: For now only checks physical needs
    
    '''
    
    physical = check_physical(agent.members)
    

    return physical

################################################################
#
#    MAIN FUNCTION
#
#################################################################


def complete_tasks(agent, hour, shops, visits, criminal, work_p):
    
    physical = check_status(agent)
    actions.select_action(physical, agent, hour, shops, visits, criminal, work_p)