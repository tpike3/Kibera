# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 10:47:01 2018

@author: ymamo
"""

#Read in dependencies
import pandas as pd
import numpy as np
import random


#########################################
#
#          HELPER FUNCTIONS
#        
#          MAIN FUNCTION LINE 317
#
############################################

# Get total number of men

def get_breakdown(row):
    
    ##########################################################
    #
    # Task: Get number of men per structre from data
    #
    # Data does not supply number of men only
    # total population, women and childred ( younger than 18) 
    # method determines numbe rof men based on subtracting 
    # women and children, substracted form total 
    #
    ######################################################
    
    total = row["POP_R"]
    women = row["WOMEN"]
    children = row["CHILD"]
    men = total - (women + children)
    return men, women, children

# create an array  of reasonable rents

def calc_rent(families, rent_mean, rent_min, rent_max):
    
    ###############################################
    #
    # Task: Create an array of rents for families
    #
    # Method: create an array based on a nornal disitrbution using
    # data input of rent mean and and range rule of (max-min) /4 
    # for standard deviation 
    #
    ##############################################   
    
    rent_distro = []
    #use range rule to calculate SD
    sd = (rent_max - rent_min)/4
    for fam in range(int(families)): 
        rent_distro.append(int(random.gauss(rent_mean, sd)))
   
    
    #rent_distro.sort() 
          
    return rent_distro


def calc_children(num_child, num_families):

    ####################################################
    #
    #
    # Task: Create an array of children values for families based on poisson distribution
    #
    # Method: lamdba calibrated through 100 runs to match number of children in dataset
    # average was 0.95 
    #
    ####################################################################
    if num_families == 0: 
        return int(num_child)
    else: 
        child_array = np.random.poisson(0.95, num_families)
        if sum(child_array) > num_child:
            while sum(child_array) > num_child:
                idx = random.randint(0, len(child_array))
                if child_array[idx-1] > 0:
                    child_array[idx-1] -= 1
        elif sum(child_array) < num_child:
            while sum(child_array) < num_child:
                idx = random.randint(0, len(child_array))
                child_array[idx-1] += 1
        else: 
            pass

        #print (child_array.tolist())
        
        return child_array.tolist()

##################################################################
#           Helper functions for parent helper function 
##################################################################
        
def divvy_men(num_men, array, level, single, deployed, s_par):
    
    ############################################################
    #
    # Task: Assign men to each family based on category
    #
    # Method: Keep assinging to each category while men still avialable to 
    # be assigned
    #
    ##############################################################
    
    #print ("SET_UP", num_men, array, single, deployed, s_par)
    while num_men > level: 
        if single > 0: 
            array[6] += 1
            num_men -= 1
            single -= 1
            if num_men == 0:
                break
        if deployed > 0: 
            array[8] += 1
            num_men -=1
            deployed -= 1
            if num_men == 0:
                break
        if random.randint(0,2) > 0 and s_par > 0: 
        #if s_par > 0: 
            array[4] += 1
            num_men -=1
            s_par -=1
            if num_men == 0:
                break
    return num_men, array, single, deployed, s_par

def divvy_women(num_w, array, level, single, deployed, s_par, poly):
    
    ############################################################
    #
    # Task: Assign women to each family based on category
    #
    # Method: Keep assigning to each category while women still avialable to 
    # be assigned
    #
    ##############################################################   
    
    while num_w > level: 
        if s_par > 0: 
            array[5] += 1
            num_w -=1
            s_par -=1
            if num_w == 0:
                break
        if poly > 0: 
            array[3] += 1
            num_w -= 1
            poly -= 1
            if num_w == 0:
                break
        if deployed > 0: 
            array[9] += 1
            num_w -=1
            deployed -= 1
            if num_w == 0:
                break
        if single > 0: 
            array[7] += 1
            num_w -= 1
            single -= 1
            if num_w == 0:
                break
        
    return num_w, array, single, deployed, s_par, poly

    
def calc_parents(total, s_par, both_par, single, poly, deployed, men, women, house):
    
    ##############################################################################
    #
    # Task: Place number of men and woemn in house for an array
    #
    # Method: Use below array strcuture to divide up type of men/women role fromm data
    #
    #array breakdown 0 = both_par_m,1 =both_par_w, 2 = poly_m, 3 = poly_w, 4= s_par_m, 5 = s_par_w,
    #6= single_m, 7 = single_w, 8 = deployed_m, 9 = deployed_w
    #
    # Uses 2 helper functions:
    # 1. divvy_men
    # 2. divvy women 
    #
    #################################################################################

    
    fam_array = [0,0,0,0,0,0,0,0,0,0]
    fam_array[0] = both_par
    men -= both_par
    fam_array[1] = both_par
    women -=both_par
    fam_array[2] = poly
    men -= poly
    fam_array[3] = 2*poly
    women -= 2*poly
    #print (fam_array)
    #fix error in women count
    if women < 0: 
        while women < 0: 
            women += 1
            men -= 1
            #print ("House " + str(house) + " data mismatch!")
            #print ("INPUT", total, s_par, both_par, single, poly, deployed, men, women)
    if men < 0: 
        while men < 0: 
            women -= 1
            men += 1
            #print ("House " + str(house) + " double female family!")
            #print ("INPUT", total, s_par, both_par, single, poly, deployed, men, women)
    #Each contains helper function for dividng up men and women
    
    if women > 3: 
        women, fam_array, single, deployed, s_par, poly = divvy_women(women, fam_array,3, single, deployed, s_par, poly)
    #print ("test array", fam_array)
    if men > 2: 
        men, fam_array, single, deployed, s_par = divvy_men(men, fam_array,2, single, deployed, s_par)
    #print ("test array", fam_array)
    if women > 2: 
        women, fam_array, single, deployed, s_par, poly = divvy_women(women, fam_array,2, single, deployed, s_par, poly)
    if men > 1: 
        men, fam_array, single, deployed, s_par = divvy_men(men, fam_array,1, single, deployed, s_par)
    if women > 1: 
        women, fam_array, single, deployed, s_par, poly = divvy_women(women, fam_array,1, single, deployed, s_par, poly)
    if men > 0: 
        men, fam_array, single, deployed, s_par = divvy_men(men, fam_array,0, single, deployed, s_par)
    if women > 0: 
        women, fam_array, single, deployed, s_par, poly = divvy_women(women, fam_array,0, single, deployed, s_par, poly)
        
    return fam_array

def get_child(children):
    
    
    #####################################################
    #
    # Tasks: Helper function to assign children
    #
    # Method: go through array and assign number of children to family
    #
    #######################################################
    
    #print (children)
    if sum(children) > 0: 
        idx = random.randint(0,len(children))-1
        if children[idx] > 0:
            child = children[idx]
            children.pop(idx)
            #print ("ROW 1:", child, children)
            return child, children
        else: 
            for i in children: 
                if i >= 1: 
                    children.pop(children.index(i))
                    return i, children
    else: 
        children.pop(0)
        #print ("ROW 3", child, children)
        return 0, children
    
def remove_child(children):
    
    ######################################################
    #
    #
    # Task: Remove children form calcuated array
    #
    # Method: Remove child and combine with other children to account for families in dictionary
    # without children (i.e. signle adults)
    #
    # Also has a debug section 
    #
    ########################################################
    
    
    #print (children)
    if 0 not in children: 
        if len(children) > 1: 
            children[1] = children[0] + children[1]
            children.pop(0)
            return children
        else:  
            children.append(True)
            return children
    else: 
        for i in children: 
            if i == 0: 
                children.pop(children.index(i))
                return children
        
    
## Function to place families in dictionary

def row_to_dict(num_fams, rent, children, parent,agent_dict, fam_num, house):
    
    #############################################################
    #
    # Task: Assign family to dictionary
    #
    #
    #Method: based on data about family type create a dictionary of each family and 
    # place key data in dictionary
    #
    ##############################################################
    
    
    #print (num_fams, rent, children, parent, house)
    rent_hold = min(rent)
    #add single males to dictionary
    for single_m in range(parent[6]):
        fam_num += 1
        children = remove_child(children)
        agent_dict[fam_num] = {"Father": 1, "Mother": 0, "Children": 0,
                               "Structure" : house, "Rent" : rent[0]}
        rent.pop(0)
        
        
    #add single females to dictionary
    for single_w in range(parent[7]):
        fam_num += 1
        children = remove_child(children)
        agent_dict[fam_num] = {"Father": 0, "Mother": 1, "Children": 0,
                               "Structure" : house, "Rent" : rent[0]}
        rent.pop(0)
        
        
        
    #add deployed male to dictionary
    for single_m in range(parent[8]):
        fam_num += 1
        children = remove_child(children)
        agent_dict[fam_num] = {"Father": 1, "Mother": 0, "Children": 0,
                               "Structure" : house, "Rent" : rent[0]}
        rent.pop(0)
        
        
    #add deployed female to dictionary
    for single_w in range(parent[9]):
        fam_num += 1
        children = remove_child(children)
        agent_dict[fam_num] = {"Father":0 , "Mother": 1, "Children": 0,
                               "Structure" : house, "Rent" : rent[0]}
        rent.pop(0)
        
    #get single male parent families
    for single_par_m in range(parent[4]):
        fam_num += 1
        #print (type(children))
        child, children = get_child(children)
        agent_dict[fam_num] = {"Father": 1, "Mother": 0, "Children": child,
                               "Structure" : house, "Rent" : rent[0]}
        rent.pop(0)
        
    #get single female parent families
    for single_par_w in range(parent[5]):
        fam_num += 1
        #print (type(children))
        child, children = get_child(children)
        agent_dict[fam_num] = {"Father": 0, "Mother": 1, "Children": child,
                              "Structure" : house, "Rent" : rent[0]}
        rent.pop(0)
        
    #get married parents
    for married_coup in range(int(parent[0])):
        fam_num+= 1
        agent_dict[fam_num] = {"Father": 1, "Mother": 1, "Children": children[0],
                               "Structure" : house, "Rent" : rent[0]}
        rent.pop(0)
        children.pop(0)
     
    #get polygamous couples
    if parent[2] > 0: 
        num_wives = parent[3]/parent[2]
        remainder = parent[3] % parent[2]
    for poly in range(int(parent[2])):
            fam_num+=1
            if remainder > 0: 
                agent_dict[fam_num] = {"Father": 1, "Mother": (num_wives + 1) , "Children": children[0],
                                       "Structure" : house, "Rent" : rent[0]}
                remainder -=1
                rent.pop[0]
                children.pop(0)
            else: 
                agent_dict[fam_num] = {"Father": 1, "Mother": num_wives , "Children": children[0],
                                       "Structure" : house, "Rent" : rent[0]}
                rent.pop(0)
                children.pop(0)
        
    if len(children) > 1: 
        #print (children)
        if children[-1] == True:
            rent_spl = rent_hold/children[0]
            for new_fam in range(children[0]):
                #print (fam_num)
                fam_num += 1
                agent_dict[fam_num] = {"Father": 0, "Mother": 0, "Children": 1,
                               "Structure" : house, "Rent" : rent_spl}
                
    #print (fam_num, num_fams)
    return agent_dict, fam_num


def extract_business(i, b_dict):
    
    #########################################################
    #
    # Task:  Extract any business form structure
    #
    #Method: Key : STR_CODE
    # Value: Dictionary of business or service types and number
    #
    ##########################################################   
    
    bus = i[1]["STR_CODE"]
    if bus not in b_dict.keys(): 
        b_dict[bus] = {"BUS_COM" : i[1]["BUSI_C"], "BUSI_PRO" : i[1]["BUSI_P"],
                                  "BUSI_S" : i[1]["BUSI_S"], "SERV_EDU": i[1]["SERV_EDU"],
                                  "SERV_H": i[1]["SERV_H"], "SERV_O": i[1]["SERV_O"]}
    else: 
        #print ("BUSINESS ELSE")
        b_dict[bus]["BUS_COM"] += i[1]["BUSI_C"]
        b_dict[bus]["BUSI_PRO"] += i[1]["BUSI_P"]
        b_dict[bus]["BUSI_S"] += i[1]["BUSI_S"]
        b_dict[bus]["SERV_EDU"] += i[1]["SERV_EDU"]
        b_dict[bus]["SERV_H"] += i[1]["SERV_H"]
        b_dict[bus]["SERV_O"] += i[1]["SERV_O"]
        
    
    return b_dict


def calc_owners(row, owner_dict): 
    
    #######################################################
    # 
    #Task: get number of owners in each structure
    #
    # Method: Create dictionary
    #Format of dict
    # KEY = "STRUCTURE"
    #VALUES = [FAMILIES], [OWNER]
    #######################################################    
    
    owner = row[1]["STR_CODE"]
    if owner not in owner_dict.keys(): 
        owner_dict[owner] = []
        owner_dict[owner].append(float(row[1]["FAMILIES"]))
        owner_dict[owner].append(float(row[1]["OWNER"]))
    else: 
        
        owner_dict[owner][0] += float(row[1]["FAMILIES"])
        owner_dict[owner][1] += float(row[1]["OWNER"])
            
       
    return owner_dict

def extract_infra(row, infra_dict):
    
    #############################################################
    #
    # Task: Get infrastrucutre per structure
    #
    # Methods: create dictionary
    # Key: Structure
    # Value: Type of infrastrucutre and number
    ############################################################
    
    struc = row[1]["STR_CODE"]
    if struc not in infra_dict.keys(): 
        infra_dict[struc] = {"ELEC": row[1]["ELECT"], "TOILET": row[1]["TOILET"], "WATER": row[1]["WATER"]}
    else: 
        #print ("INFRA ELSE")
        infra_dict[struc]["ELEC"] += row[1]["ELECT"]
        infra_dict[struc]["TOILET"] += row[1]["TOILET"]
        infra_dict[struc]["WATER"] += row[1]["WATER"]
        
    #print (infra_dict)
    return infra_dict


##############################################################################
##
##              MAIN FUNCTION 
##
##############################################################################


def get_Agents_Phase1(df):
    
    print ("\n", "Beginning Phase I: Reading in .shp database file", "\n")
    print ("READING IN DATA and MAKING FAMILIES")
    ##################################################################
    #
    # Task: Create a dictionary of each family
    #
    # Method: Iterate through strucutres in data and divde them into specific strcutures while documenting 
    # infrastrucutre and ownership for use in phase 2
    #
    # Dictionary structure: 
    # Key: Fmailiy number based on when read in 
    #Value: Dictionary - Father, Mother, CHildren, strcuture they are assigned  and 
    # house, business and infrastructure if applicable
    #
    #####################################################################
    
    #  Fix some issues with data
    #Account for 2 women in one house (assume multi-generational or sisters--data counts as both parents,
    #or prostitution ring with madams)
    df.at[126,"FAM_S"] = 1
    df.at[126,"FAM_C"] = 0
    df.at[126,"FAM_SP"] = 1
    df.at[126,"FAM_S"] = 1
    df.at[126,"FAMILIES"] = 2
    
    #Account for polygamous family at 432 where numbers do not add up
    df.at[432,"FAM_SP"] = 1
    df.at[432,"FAM_C"] = 0
    df.at[432,"FAM_P"] = 1
    
    #Delete random owner in upopulated house with no other data
    df.at[26, "OWNER"] = 0
    
    infra_dict = {}
    business_dict = {}
    owner_dict = {}
    agent_dict = {}
    fam_num = 0
    
        
    for i in df.iterrows(): 
        
                
        #print (i[0])
        num_fams = int(i[1]["FAMILIES"])
        #print (num_fams)
        #use helper function get_breakdown to calculate men
        men, women, children = get_breakdown(i[1])
        #print ("gender_break", men, women, children, "\n")
        #use helper function calc rent to calculate rent for family
        rent = calc_rent(i[1]['FAMILIES'], i[1]["RENT_MEAN"], i[1]["RENT_MIN"], i[1]["RENT_MAX"])
        #print ("RENT", rent,i[1]["RENT_MIN"], i[1]["RENT_MAX"],"\n")
        child_array = calc_children(i[1]["CHILD"], int(i[1]["FAMILIES"]))
        #print ("CHILD ARRAY", sum(child_array), i[1]["CHILD"], child_array)
        fam_parent_array = calc_parents(i[1]["FAMILIES"], i[1]["FAM_SP"], i[1]["FAM_C"],i[1]["FAM_S"], i[1]["FAM_P"],
                                        i[1]["FAM_UP"], men, women, i[0])
        #array breakdown 0 = both_par_m,1 =both_par_w, 2 = poly_m, 3 = poly_w, 4= s_par_m, 5 = s_par_w,
        #6= single_m, 7 = single_w, 8 = deployed_m, 9 = deployed_w
        #print ("FAM PARENT ARRAY", fam_parent_array)
        #print ( i[1]["FAM_C"], i[1]["FAM_UP"], i[1]["FAM_SP"], i[1]["FAM_S"], i[1]["FAM_P"], "\n")
        #account for children living on their own
        if type(child_array) == int:
            for g in range(child_array):
                fam_num += 1
                agent_dict[fam_num] = {"Father": 0, "Mother": 0 , "Children": 1,
                                           "Structure" : i[1]["STR_CODE"], "Rent" : (i[1]["RENT_MEAN"]/child_array)}
        else: 
            agent_dict, fam_num = row_to_dict(num_fams, rent, child_array, fam_parent_array, agent_dict, fam_num, i[1]["STR_CODE"])
            
        #business dictionary for use in build, agent pahse 2
        if i[1]["BUSINESS"] > 0 or i[1]["SERVICE"]> 0:
            business_dict = extract_business(i, business_dict)
            
        if i[1]["OWNER"] > 0: 
            owner_dict = calc_owners(i, owner_dict)
            
        if i[1]["ELECT"] > 0 or i[1]["WATER"] > 0 or i[1]["TOILET"] > 0: 
            infra_dict = extract_infra(i, infra_dict)
        
    print ("ALL DATA READ IN. YOU HAVE " + str(len(agent_dict.keys())) + " FAMILIES.")
    
    #print (business_dict)
    b_com = 0
    for v in business_dict.values(): 
        b_com += v["BUS_COM"]
    #print ("BUSINESS COMMERCIAL ", b_com)
    
    #print (owner_dict)
    #stop
    
    return agent_dict, business_dict, owner_dict, infra_dict
        
    

