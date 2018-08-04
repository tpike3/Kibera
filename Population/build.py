# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 13:17:39 2018

From Dictionary of families add additional attributes 

create a dictionary of agents

CSS 645
Tom Pike
"""

import random
import pandas as pd
from simpledbf import Dbf5 
import copy

def test(fam_str):
    for i in fam_str.values():
        if len(i) == 0:
            print ("NO FAMILIES")


#############################################
#
#          HELPER FUNCTIONS
#
#          MAIN FUNCTION AT line 453
#
############################################

def print_agentclass(agents):
    
    lower = 0
    middle = 0
    upper = 0
    for v in agents.values(): 
        if v["Class"] == "Lower":
            lower += 1
        if v["Class"] == "Middle":
            middle += 1
        if v["Class"] == "Upper":
            upper += 1
    
    print ("Lower Class: ", lower)
    print ("Middle Class: ", middle)
    print ("Upper Class: ", upper)
    print ("")


def add_Tribes(agents):
    
    '''
    KIBERA PERCENTAGES
    Tribes (number of families)
    Luo: 2,196 (36.5%)
    Kisii: 689 (11.5%) 
    Luhya: 661 (11.0%)
    Kamba: 427 (7.1%)
    Gikuyu: 247 (4.1%)
    Other tribes or unknown: 1,801 (29.8%)    
    '''
    tribe_array = []
    
       
    #print (agents.keys())
    #calculate families    
    num_fam = len(agents.keys())
    #print (num_fam)
    #calculate numbers
    num_Luo = int(num_fam * .365)
    num_Kisii = int(num_fam * .115)
    num_Luhya = int(num_fam * .11)
    num_Kamba = int(num_fam * .071)
    num_Kikuyu = int(num_fam * .041)
    ##UNKNOWN
    num_Kalenjin = int(num_fam * .031)
    other_tribes = num_fam - (num_Luo + num_Kisii + num_Luhya + num_Kamba + num_Kikuyu + num_Kalenjin)
    #print (other_tribes)
    other_unknown = ['KAMBA', 'TAITA', 'TAVETA', 'TURKANA', "MASAI", "TESO", "MERU", "UGANDA", "TANZANI", "OTHER", "UNKNOWN"]
    split = int(other_tribes/len(other_unknown))
    

    
    #add Kikuyu
    tribe_array += ["Kikuyu" for x in range(num_Kikuyu)]
    kikuyu_assigned = []
    #print ("LEN TRIBES-pre-Kikuyu", len(tribe_array))
    
    #assign Kikuyu as owners
    for key, fam in agents.items():
        if len(tribe_array) > 0: 
            if "BUSINESS" in fam or "OWN_HOUSES" in fam:
                #print (fam)
                agents[key]["Tribe"] = tribe_array[0]
                tribe_array.pop(0)
                kikuyu_assigned.append(key)
        
            
    #print (len(kikuyu_assigned))            
    #print ("LEN TRIBES-post-Kikuyu", len(tribe_array))
    #add Luo
    tribe_array += ["Luo" for x in range(num_Luo + 4)]
    #add Kisii
    tribe_array += ["Kisii" for x in range(num_Kisii + 4)]
    #add_Luhya
    tribe_array += ["Luhya" for x in range(num_Luhya)]
    #add Kamba
    tribe_array += ["Kamba" for x in range(num_Kamba)]
    #add Kalenjin
    tribe_array += ["Kalenjin" for x in range(num_Kalenjin)]
    #add other unknown
    for other in other_unknown: 
        tribe_array += [ other for x in range(split)]      
     
    #print ("LEN TRIBES", len(tribe_array), "num_families ", num_fam)
    #ensure array is well shuffled
    for i in range(5):
        random.shuffle(tribe_array)
    #print (len(tribe_array))  
    
    
    count = 0
    for fam_num in agents.keys() : 
        if fam_num in kikuyu_assigned: 
            count+=1
        else: 
            
            agents[fam_num]["Tribe"] = tribe_array[0]
            tribe_array.pop(0)
            count+=1
        #print (count)
            #print (len(tribe_array)) 

    #print (tribe_array)
    
    print ("TRIBES ASSIGNED")
    return agents
    #for fams in agents.values(): 

def make_famstr(agents):

    #make family, structure dictionary for faster, cleaner data tranformation
    #########################################################################
    #
    # Strucutre is 
    #Key: Structure Code
    # Value: List of Family numbers
    #
    #####################################################################
    
    fam_str = {}
    for fam,val in agents.items():
        if val["Structure"] not in fam_str.keys(): 
            fam_str[val["Structure"]] = [fam]
        else: 
            fam_str[val["Structure"]].append(fam)

    #print ("TEST 1")
    #test(fam_str)
    
    return fam_str

def get_businesses(busi): 
    
    business_list = []
    for key, value in busi.items(): 
        if value > 0: 
            for i in range(int(value)):
                business_list.append(key)
    #print (business_list)    
    return business_list

def reduce_struct(struct):
    
    #Helper function for check_struct to reduct to larger structure
    f_struct = ''
    if struct[0] == "K":
        f_struct = struct[6:]
        
        for i in f_struct: 
            if i == "S":
                end = f_struct.index(i)
        f_struct = f_struct[:end]
    else: 
        f_struct = struct[4:]
        
        for i in f_struct: 
            if i == "S":
                end = f_struct.index(i)
        f_struct = f_struct[:end]
        
    return f_struct
    


def check_struct(struct, strs_w_fam):
    
    #reduce struture with no family to larger strucutre number
    f_struct = reduce_struct(struct)
    
    #reduce structs with families to possibles
    containing_structs = []
    for each in strs_w_fam: 
        if f_struct in each: 
            containing_structs.append(each)
    
    #get substrucutres in larger structure
    possible_structs = []
    for each in containing_structs:
        p_struct = reduce_struct(each)
        if p_struct == f_struct: 
            possible_structs.append(each)
        
    
    #print (f_struct)
    #print (possible_structs)

    return possible_structs

def assign_businesses(agents, busi, owners, fam_str, strs_with_owners, strs_w_fam): 
    
    
    str_noFam = []
    assigned_structures = []
    #add business to agent families
    for struct, busi in busi.items(): 
        
        #get business options from helper list
        business_list = get_businesses(busi)        #######Helper function
        #print (business_list)
        random.shuffle(business_list)
        #get owners from owner_dict
        if struct in strs_with_owners: 
            own_1 = copy.copy(owners[struct])
        else: 
            own_1 = "NONE"
        #get family list
        if struct in strs_w_fam: 
            fam_2 = copy.copy(fam_str[struct])
            random.shuffle(fam_2)
        else: 
            #account with business no families in structure
            #see if in a full structure
            
            sub_structs = check_struct(struct, strs_w_fam)                  ####HELPER FUNCTION 
            fam_2 = []
            for each in sub_structs:
                fam_2 += fam_str[each]
            if len(fam_2) == 0:    
                str_noFam.append(struct)
                fam_2 = "NONE"
            #print (fam_2)
            
            #str_noFam.append(struct)
            #fam_2 = "NONE"
            #print (business_list)
        
        if own_1 != "NONE" and fam_2 != "NONE":
                                    
            if own_1[1] > len(business_list):
                #print (own_1[1], business_list)
                
                #get number of owners which are not businesses (must own own house)
                own_house = int(own_1[1] - len(business_list))
                #make seperate fam_2 list; 
                fam_3 = []
                
                while len(business_list) > 1: 
                    agents[fam_2[0]]["BUSINESS"] = business_list[0]
                    business_list.pop(0)
                    #assume is they own the business they own the house
                    fam_3.append(fam_2[0])
                    fam_2.pop(0)
                    
                #make sure enough families are in list to account for all additional owners
                while len(fam_3) < own_house:
                    fam_3.append(fam_2[0])
                    fam_2.pop(0)
                
                #Assign ownership of houses
                random.shuffle(fam_3)
                for i in range(own_house):
                    agents[fam_3[0]]["OWN_HOUSES"] = struct
                    fam_3.pop(0)
                
                    
            else: 
                #print (len(fam_2), own_1[1], len(business_list))
                for i in range(len(business_list)):                    
                    if len(fam_2) > 0:
                        agents[fam_2[0]]["BUSINESS"] = business_list[0]
                        business_list.pop(0)
                        fam_2.pop(0)
        
        assigned_structures.append(struct)
    #print (len(assigned_structures))
        
    #print ("BUSINESS NO FAMS ", str_noFam) 
        
    
    return agents, assigned_structures


def assign_ownership(agents, bus_structs, owners, fam_str):
        
    for struct, owners in owners.items():
        if struct in bus_structs or struct not in fam_str.keys(): 
            pass
        else: 
            
            #assigns ownership to houses
            fam_poss  = copy.copy(fam_str[struct]) 
            random.shuffle(fam_poss)
            for fam in range(int(owners[1])):
                agents[fam_poss[0]]["OWN_HOUSES"] = struct
                fam_poss.pop(0)
    #print ("Test 3")
    #test(fam_str)
    return agents


def add_Busi(agents,busi, owners):
       
    #helper function to make easier family structure data dynamic    
    fam_str = make_famstr(agents)    
    #cache list of structures
    strs_w_fam = fam_str.keys()     
    #print (len(strs_w_fam))
    #cache list of owners 
    strs_with_owners = owners.keys()
    
    #for debugging
    no_owners = []
    
    for house in strs_with_owners: 
        if house not in strs_w_fam: 
            no_owners.append(house)
    
    #print ("NO OWNERS: ", len(no_owners))
    
    #Get businesses
    agents, bus_structs = assign_businesses(agents, busi, owners, fam_str,strs_with_owners, strs_w_fam)
    agents = assign_ownership(agents, bus_structs, owners, fam_str)

     
    count_b = 0
    count_o = 0
    for i in agents.values(): 
        if "BUSINESS" in i: 
            
            count_b += 1
        if "OWN_HOUSES" in i:
            #print (i)
            count_o += 1
    print ("FAMILIES WHO OWN BUSINESSES:" , count_b)
    print ("FAMILIES WHO OWN HOUSES: ", count_o )
    
      
    return agents

def get_fam_precedent(fam_list, agents):
        
    #get precedent list based on owership of families
    #shuffle to ensure mix
    random.shuffle(fam_list)
    
    fam_prec = []
    
    #Priority one own houses and Business
    
    for fam in fam_list:
        
        if "BUSINESS" in agents[fam] and "OWN_HOUSES" in agents[fam]:
            idx = fam_list.index(fam)
            fam_prec.append(fam)
            fam_list.pop(idx)
    
           
    for fam in fam_list: 
        #print ("2", fam_list) 
        if "BUSINESS" in agents[fam] or "OWN_HOUSES" in agents[fam]:
            idx = fam_list.index(fam)
            fam_prec.append(fam)
            fam_list.pop(idx)
            
    for fam in fam_list: 
        fam_prec.append(fam)
        
    #print (fam_prec)
    return fam_prec



def add_infra(agents, infra):
    
     #assign water and toilet infrastructure
    
    fam_str = make_famstr(agents)
   
    for k,v in infra.items(): 
        if k in fam_str.keys():
            fam_prec = get_fam_precedent(fam_str[k], agents)
            if v["WATER"] > 0: 
                
                if len(fam_prec) > v["WATER"]:
                    for i in range(int(v["WATER"])):
                        agents[fam_prec[i]]["WATER"] = 1
                else:
                    p_water =  v["WATER"]/len(fam_prec)
                    p_water_2 =  v["WATER"] % len(fam_prec)
                    for fam in fam_prec:
                            agents[fam]["WATER"] = p_water
                    
                    idx = 0
                    while p_water_2 > 0: 
                        agents[fam_prec[idx]]["WATER"] += 1
                        p_water_2 -= 1
                        idx +=1
                        
            if v["TOILET"]  > 0:
                #print (fam_prec, fam_str[k])
                if len(fam_prec) > v["TOILET"]:
                    for i in range(int(v["TOILET"])):
                        agents[fam_prec[i]]["TOILET"] = 1
                else:
                    p_toilet =  v["TOILET"]/len(fam_prec)
                    p_toilet_2 =  v["TOILET"] % len(fam_prec)
                    for fam in fam_prec:
                            agents[fam]["TOILET"] = p_toilet
                    
                    idx = 0
                    while p_toilet_2 > 0: 
                        agents[fam_prec[idx]]["TOILET"] += 1
                        p_toilet_2 -= 1
                        idx +=1
                        
            if v["ELEC"] > 0: 
                if len(fam_prec) > v["ELEC"]:
                    for i in range(int(v["ELEC"])):
                        agents[fam_prec[i]]["ELEC"] = 1
                else:
                    p_elec =  v["ELEC"]/len(fam_prec)
                    p_elec_2 =  v["ELEC"] % len(fam_prec)
                    for fam in fam_prec:
                            agents[fam]["ELEC"] = p_elec
                    
                    idx = 0
                    while p_elec_2 > 0: 
                        agents[fam_prec[idx]]["ELEC"] += 1
                        p_elec_2 -= 1
                        idx +=1
    count_w = 0
    count_t = 0
    count_e = 0                
    for v in agents.values(): 
        if "WATER" in v: 
            count_w += 1
        if "TOILET" in v: 
            count_t += 1
        if "ELEC" in v: 
            count_e += 1
    print ("FAMILIES WITH WATER: ", count_w)
    print ("FAMILIES WITH TOILETS: ", count_t)
    print ("FAMILIES WITH ELECTRICITY: " , count_e)
    
    return agents

def assign_class(agents): 
    
    ################################################
    #
    # Task: Assign class value to agents to support job allocation
    #
    #Process: Upper class own business, houses
    # middle: less than 4 kids, have electricity/water
    # lower: lots of kids or single no infrastructure 
    #
    ###################################################
    
    for k, v in agents.items(): 
        if "BUSINESS" in v or "OWN_HOUSES" in v: 
            agents[k]["Class"] = "Upper"
        elif "WATER" in v or "ELEC" in v or "TOILET" in v: 
            agents[k]["Class"] = "Middle"
        else: 
            agents[k]["Class"] = "Lower"
            
    return agents
                   
#########################################
##
##        MAIN FUNCTION
##
##########################################


def agents_Phase2(agents, businesses, owners, infra):
    '''
    DICTIONARY STRUCTURE
    {"Father": N, "Mother": N, "Children": N,
     "Structure" : STR, "Rent" : INT}
    '''
    #account 3 children in structure 0S2S151S80; rent min in data
    for k,v in agents.items():
        if v["Rent"] == 0:
            v["Rent"] = 670/3
    
    print ("\n", "Beginning Phase II: Assigning families, structures and tribes ", "\n")
    
    agents_wowners = add_Busi(agents, businesses, owners)   
    agents_watertoilets = add_infra(agents_wowners, infra)
    agents_wtribes = add_Tribes(agents_watertoilets)
    agents_wclass = assign_class(agents_wtribes)
    print ("\nEconomic class structure by family:")
    print_agentclass(agents_wclass)
    
    '''
    for i in range(842, 847):
        print (agents[i])
    '''
    
    return agents_wclass
