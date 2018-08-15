# -*- coding: utf-8 -*-
"""
Created on Mon May 14 05:50:57 2018

Tom Pike
CSS645
Data Export
"""

import pandas as pd
from itertools import product


def runs():
    
    runs_t = []
    #initial = []
    pay = []
    prob = [ .5] #, .5, .7] #[0.8, 0.9,
      
    for i in [25]: #[10, 20, 25, 30]: #[ 30, 35, 40, 45] [50, 70, 90]:#,[50, 60, 70, 80, 90, 100, 110]:
    #for i in range(110,120,10):
        pay.append(i)
        
    
    runs_t = product(pay, prob)
    
    return runs_t



def exportdata(data):
    
    col = ["Run", "Initial Wealth", "Pay Multiplier", "Probability", \
                               "Day", "3 Meals", "2 Meals", "1 Meal", "0 Meals", "Variety 4",\
                               "Variety 3", "Variety 2", "Child Labor", "Meal Cost", \
                               "Wealth Distro","Steal", "Meal Distro", "Child 2"]
    df =pd.DataFrame()
    
    df_run= {}
    for k,run in data.items():
        for d, v in run.items():
            df_run["Run"] = k[0]
            df_run["Pay Multiplier"] = k[1]
            df_run["Probability"] = k[2]
            df_run["Day"] = d
            df_run["3 Meals"] = v[0]["3 Meals"]
            df_run["2 Meals"] = v[0]["2 Meals"]
            df_run["1 Meal"] = v[0]["1 Meal"]
            df_run["0 Meals"] = v[0]["0 Meals"]
            df_run["Variety 4"] =v[1]["4 Food Types"]
            df_run["Variety 3"] =v[1]["3 Food Types"]
            df_run["Variety 2"] =v[1]["2 Food Types"]
            df_run["Child Labor"] = v[2]
            df_run["Meal Cost"] = v[3]
            df_run["Wealth Distro"] = v[4]
            df_run["Steal"] =v[5]
            df_run["Meal Distro"] = v[6]
            df_run["Child 2"] =v[7]
                       
                        
            
            df = df.append(df_run, ignore_index = True)
            df_run = {}
            
              
           
    df.to_csv("C:\\Users\\ymamo\\Kibera\\Results\\Kianda Output.csv")
        
    
    
    
 
print ("Number of Runs: ", len(list(runs())))