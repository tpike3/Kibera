# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:51:21 2018

@author: ymamo
"""

#########################################
#
# HELPER FUNCTION
#
########################################

def add_family(families):
    
    

##########################################
#
# MAIN FUNCTION 
#
##########################################


def make_families(agents):
    
    families = {}
    
    for k,v in families.items(): 
        
        if v["Family"] not in families: 
            
            families[v["Family"]] = {}
            families = add_family(families, k, v)
            
        else: 
            families = add_family(families, k, v)
            
    return families