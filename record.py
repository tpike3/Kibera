# -*- coding: utf-8 -*-
"""
Created on Sat May 12 06:03:30 2018

@author: ymamo
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

class Record(object):
    
    def __init__(self):
        
        self.fig, self.axarr = plt.subplots(2,2, figsize=(15,15))
        self.fig.suptitle("Kianda Population Patterns", fontsize=14, fontweight='bold') 
        self.axarr[0,0].set_title("Meals Per Day")
        self.axarr[0,0].set_xticks(np.arange(1,5))
        self.axarr[0,0].set_xticklabels(["3 Meals", "2 Meals", "1 Meal", "0 Meals"])
        self.ind = np.arange(1,5)
        self.axarr[0,1].set_title("Meal Variety")
        self.axarr[0,1].set_xticks(np.arange(1,5))
        self.axarr[0,1].set_xticklabels(["4 Food Types", "3 Food Types", "2 Food Types"])
        self.axarr[1,0].set_title("Percent Child Labor")
        plt.show()
   


    
    def update_bar(self, meals, variety):
        total = meals["3 Meals"]+ meals["2 Meals"]+ meals["1 Meal"] + meals["0 Meals"] # \
               # + meals["3_partial"] + meals["2_partial"] + meals["1_partial"]
        p_3 = str(round(((meals["3 Meals"])/ total) *100))
        p_2 = str(round(((meals["2 Meals"])/ total) *100))
        p_1 = str(round(((meals["1 Meal"] + meals["0 Meals"])/ total) *100))
        
        self.axarr[0,0].bar(self.ind, [meals["3 Meals"], meals["2 Meals"], meals["1 Meal"], meals["0 Meals"]], color= "g")
        self.axarr[0,0].text(3 , 1300, "3 Meals = " + p_3 +"%\n2 Meals = " + p_2 + "%\n0-1 Meals = " + p_1 +"%")
        
        self.axarr[0,1].bar(np.arange(1,4), [variety["4 Food Types"], variety["3 Food Types"], variety["2 Food Types"]], color = "b")
        
        
        