# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 14:47:33 2018
Add phenotypes which drive agent behavior


Tom Pike
CSS 645
"""

def single_decision(agent, hour): 
    
    #if step != 0 and step % 6 = 0: 
    #print ("single_decision ", hour)
    pass

def multi_decision(agent, hour):
    
    pass






def split_tasks(agent, hour):
    if len(agent.members.keys()) == 1: 
        single_decision(agent, hour)
    else: 
        multi_decision(agent, hour)
