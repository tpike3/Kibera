# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 14:51:47 2018

From Dictionary of families turn into a dictionary of agents with attributes

create agent dictionary

CSS 645
Tom Pike
"""
import math
import random
import build

###############################################
#
#
#     Helper Functions
#
##############################################

def print_demographics(women_age, men_age, female_child_age, male_child_age): 
    
    #############################################
    #
    # Task: Helper function to print distribution of ages aacross sex
    #
    # Purpose: Verfy code is working properly
    #
    ###############################################
    
    #total = 0
    print ("Your Women age demographics:")
    women = 0
    for k,v, in women_age.items(): 
        print (k,": ",  v[1])
        women += v[1]
    print ("Women Total: " , women, "\n")
    print ("Your male age demographics:")
    
    men = 0
    for k,v, in men_age.items(): 
        print (k,": ", v[1])
        men += v[1]
    print ("Men Total: " , men, "\n")
    
    print ("Your female children age demographics: " )
    for k,v in female_child_age.items(): 
        print (k, ": " , v[1])
    print ("")
    
    print ("Your male children age demographics: " )
    for k,v in male_child_age.items(): 
        print (k, ": ", v[1])
    print ("") 

    print ("Total Agents From Phase I: ", women+men+female_child_age["Total"][1]+male_child_age["Total"][1])
    
    

def make_age(families): 
    
    ########################################
    # 
    # Task: Create an array of ages based on 
    # demographic data from  
    #African Population and Health Research Center (APHRC). 2014. 
    #“Population and Health Dynamics in Nairobi’s Informal Settlements: 
    #Report of the Nairobi Cross-Sectional Slums Survey (NCSS) 2012.” Nairobi: APHRC, no. April: 1–185.
    #
    #
    # Process: 
    #  - Get number of males by age_group
    #  - Get number of females by age group
    #  
    #######################################
    
    women = 0
    for v in families.values(): 
        if v["Mother"] > 0: 
            women += int(v["Mother"])
    #print ("WOMEN", women)        
    males = 0
    for v in families.values(): 
        if v["Father"] > 0:
            males += 1
    #print ("MALES", males)
    children = 0
    for v in families.values(): 
        if v["Children"] > 0:
            children += v["Children"]
    #print ("Children", children)
    
    #numbers calculated from "Kibera: The Biggest Slum in Africa"
    children_male = int(children * .49)
    children_female = int(children * .51) + 1
    
    
    
    #decimal numbers obtained from APHRC
    #one added to highest value ages to account for rounding errors
    women_age = { "18-25": [int(.33 * women) + 1, 0], "25-50": [int(.65 * women)+1,0], 
                            "51+": [int(.02 * women)+1,0]}
    male_age= { "18-25": [int(.21 * males)+1,0], "25-50": [int(.77 * males)+1,0], "51+": [int(.02* males)+1,0]}
    
    children_male_age = {"0-4": [int(.32 * children_male), 0],"5-9": [int(.23 * children_male),0], 
                                 "10-14": [int(.23*children_male), 0],"15-18": [int(.22*children_male), 0],
                                 "Total": [children_male,0]}
    children_female_age = {"0-4": [int(.32 * children_female), 0],"5-9":[int(.23 * children_female), 0],
                                   "10-14": [int(.23*children_female), 0],"15-18": [int(.22*children_female), 0],
                                   "Total" : [children_female,0]}
                   
    '''
    print ("\n", "AGE ARRAY VALUES:" )
    print (children_male_age, children_male,  "\n")
    print (children_female_age, children_female)
    print ("")
    '''
    return women_age, male_age, children_female_age, children_male_age


def select_age(k,v,age, p_age, p_elderly):
    
    
    ###################################################################
    #
    # Task: Assign age based on biologicial reprodution processes and population 
    # demographics
    #
    # Process:
    #   If p_age less than 0.5 (less than 2 kids), place in 18-25 age bracket, else 25-50
    #   if high number of kids place in 51 brakect. If no kids most likely to be 18-25 for 51+
    #   but possibily can be 25-50.
    ########################################################################
    
    
    age_assign = ""
    
    
    if v["Children"] > 0:
        if p_age < 0.5 and age["18-25"][0] > age["18-25"][1]: 
            age_assign = "18-25"
            age["18-25"][1] += 1
        else: 
            age_assign = "25-50"
            age["25-50"][1] += 1
            
    else: 
        if age["51+"][0] > age["51+"][1]:
            #print (p)
            if p_elderly == 1: 
                age_assign = "51+"
                age["51+"][1] += 1
            else: 
               if age["18-25"][1] < age["18-25"][0]:  
                   age_assign= "18-25"
                   age["18-25"][1] += 1
               elif age["25-50"][1] < age["25-50"][0]: 
                  age_assign = "25-50"
                  age["25-50"][1] += 1 
               else:           
                   age_assign = "51+"
                   age["51+"][1] += 1
                    
        elif age["18-25"][1] < age["18-25"][0]:  
                   age_assign= "18-25"
                   age["18-25"][1] += 1
        elif age["25-50"][1] < age["25-50"][0]: 
                  age_assign = "25-50"
                  age["25-50"][1] += 1
        else:           
            age_assign = "51+"
            age["51+"][1] += 1
            
    return age_assign
            

def age_children(v, gender, age_mom, i, child_age_dict, chance): 
        
    #print (child_age_dict)
    age = ""
    diff_10_14 = (child_age_dict["10-14"][0] - child_age_dict["10-14"][1])/child_age_dict["10-14"][0]
    diff_14_18 = (child_age_dict["15-18"][0] - child_age_dict["15-18"][1])/child_age_dict["15-18"][0]
    diff_5_9 = (child_age_dict["5-9"][0] - child_age_dict["5-9"][1])/child_age_dict["5-9"][0]
    diff_0_4 = (child_age_dict["0-4"][0] - child_age_dict["0-4"][1])/child_age_dict["0-4"][0]
    
    if v["Mother"] == 0 and v["Father"] == 0: 
        #print ("FAMILY WITHOUT PARENTS") 
        if diff_10_14 <= diff_14_18:
             age = "10-14"
             child_age_dict["10-14"][1] += 1
        else: 
            age = "15-18"
            child_age_dict["15-18"][1] += 1
    elif i > 12 and child_age_dict["15-18"][1] <= child_age_dict["15-18"][0]: 
        age = "15-18"
        child_age_dict["15-18"][1] += 1    
    elif i > 4: 
        if diff_10_14 >= diff_14_18:  
                if child_age_dict["15-18"][0] >= child_age_dict["15-18"][1]:
                    age = "15-18"
                    child_age_dict["15-18"][1] += 1
        else: 
            if child_age_dict["10-14"][0] > child_age_dict["10-14"][1]: 
                age = "10-14"
                child_age_dict["10-14"][1] += 1
    else: 
        if age_mom == "18-25": 
            if child_age_dict["0-4"][0] > child_age_dict["0-4"][1]:
                age = "0-4"
                child_age_dict["0-4"][1] += 1
            else: 
                age = "5-9"
                child_age_dict["5-9"][1] += 1
        elif age_mom == "25-50": 
            #bias to older children first- based on runs which shouwed too many kids having age of 0-4
            if diff_5_9 <= diff_10_14 and child_age_dict["5-9"][0] > child_age_dict["5-9"][1]: 
                age = "5-9"
                child_age_dict["5-9"][1] += 1
            elif diff_10_14 <= diff_14_18 and child_age_dict["10-14"][0] > child_age_dict["10-14"][1]: 
                age = "10-14"
                child_age_dict["10-14"][1] += 1
            elif child_age_dict["0-4"][0] > child_age_dict["0-4"][1]:
                age = "0-4"
                child_age_dict["0-4"][1] += 1
            elif child_age_dict["15-18"][0] > child_age_dict["15-18"][1]:
                age = "15-18"
                child_age_dict["15-18"][1] += 1
            else: 
                if child_age_dict["10-14"][0] > child_age_dict["10-14"][1]:
                    age = "10-14"
                    child_age_dict["10-14"][1] += 1
    if age == "": 
        if child_age_dict["0-4"][0] >= child_age_dict["10-14"][1]:
            age = "0-4"
            child_age_dict["0-4"][1] += 1
        elif child_age_dict["10-14"][0] >= child_age_dict["10-14"][1]: 
            age = "10-14"
            child_age_dict["10-14"][1] += 1
        elif child_age_dict["5-9"][0] >= child_age_dict["5-9"][1]: 
            age = "5-9"
            child_age_dict["5-9"][1] += 1
        elif child_age_dict["15-18"][0] >= child_age_dict["15-18"][1]: 
            age = "15-18"
            child_age_dict["15-18"][1] += 1
        else:
            print ("Child Ages are off")
        
    if age == "":
       print ("Age related challenge, agentize, line 226")
       print (gender, i)
       print (child_age_dict)
    
    return age




def select_children_ga(v, female_child_age, male_child_age, age_mom, i):
    
    ##############################################################
    #
    # Task: Assign gender and age to each child
    #
    # Process: 
    #   Assign gender based on probability using demographic data 
    #   Assign age based number of chidren, age of parents and demogrpahics
    #
    ############################################################
    
    age = ""
    gender = ""
    
    ########################################################
    #
    # Assign gender 
    #
    #############################################################
        
    chance = random.random()
    
    if chance < 0.5 and female_child_age["Total"][1] < female_child_age["Total"][0]:
        gender = "F"
        female_child_age["Total"][1] += 1
    
    elif chance >= 0.5 and male_child_age["Total"][1] < male_child_age["Total"][0]: 
        gender = "M"
        male_child_age["Total"][1] += 1
        
    else: 
        if female_child_age["Total"][1] < female_child_age["Total"][0]: 
            gender = "F"
            female_child_age["Total"][1] += 1
            
        elif male_child_age["Total"][1] < male_child_age["Total"][0]: 
            gender = "M"
            male_child_age["Total"][1] += 1
        else: 
            print ("agentize, line 249, children gender assign issue")
        
    ###############################################################
    #
    #Assign age
    #
    ##################################################################
    
    
    if gender == "M": 
        age = age_children(v,gender, age_mom, i, male_child_age, chance)
    elif gender == "F": 
        age = age_children(v,gender, age_mom, i, female_child_age, chance)
    else: 
        print ("NO GENDER ASSIGNED") 
        
    return gender, age
    
##############################################################
#
# GETTERS AND SETTERS
#
##############################################################


def get_employment(v):
    
    if "BUSINESS" in v: 
        return "B_Owner"
    else: 
        return "TBD"
    
    
def get_child_employment(v, age): 
    
    if age == "0-4": 
        return "Too young"
    elif age == "5-9":
        return "Student"
    elif age == "10-14": 
        return "Student"
    elif age == "15-18": 
        return "TBD"
    else: 
        #print ("AGE:", age)
        print ("There is a child without an age.")
        return None
    
def get_water(v):

    if "WATER" in v: 
        return v["WATER"]
    else:
        return None
    
def get_electricity(v):
    if "ELEC" in v: 
        return v["ELEC"]
    else:
        return None
    
def get_toilet(v):
    if "TOILET" in v:
        return v["TOILET"]
    else: 
        return None
    
def get_rent(v): 
    if "OWN_HOUSES" in v: 
        return v["Rent"] *1.5 #used to set income later
    else: 
        return v["Rent"]
            
 ####################################################################
#
#   MAIN FUNCTION HELPER FUNCTIONS LEVEL 1
#  
#   Make male
#   Make female
#   Make children
#
#####################################################################       

def make_male(k,v,age_m, agents, agent_num, p_age,p_elderly):
    
    ###################################
    # Men from data: 5104; on website: 5088
    #
    # Tasks: Make male agents
    #
    # Process: 
    #       Assign gender 
    #       Assign age
    #       Assign size
    #       Assign
    #
    ##################################
      
    agent_num += 1
    age = select_age(k, v, age_m, p_age, p_elderly)
    agents[agent_num] = {"Gender" : "M",
                         "Family" : k,
                         "Tribe" : v["Tribe"],
                         "House": v["Structure"],
                         "Age": age, 
                         "Children" : v["Children"],
                         "Employment": get_employment(v), 
                         "Water" : get_water(v),
                         "Electricity" : get_electricity(v), 
                         "RENT": get_rent(v),
                         "Toilet" : get_toilet(v),
                         "Class" : v["Class"] }
                         
   
       
    return agents, agent_num


def make_female(k,v,age_w, agents,agent_num, p_age, p_elderly):

    ###################################
    # Women from data: 3188; on website: 3,208
    #
    # Tasks: Make female agents
    #
    # Process: 
    #       Assign gender 
    #       Assign age
    #       Assign job
    #       Assign
    #
    ##################################  
    
    age = ""
    
     
    for i in range(int(v["Mother"])):
        agent_num += 1
        age = select_age(k,v, age_w, p_age, p_elderly)
        agents[agent_num] = {"Gender" : "F", 
                              "Family" : k,
                             "Tribe" : v["Tribe"],
                             "House": v["Structure"],
                             "Age": age,
                             "Children" : v["Children"],
                             "Employment": get_employment(v),
                             "Water" : get_water(v),
                             "Electricity" : get_electricity(v), 
                             "RENT": get_rent(v), 
                             "Toilet" : get_toilet(v),
                             "Class": v["Class"]} 
                            

    return agents, agent_num, age

def make_children(k,v,female_child_age, male_child_age, agents, agent_num, age_mom): 
    
    
    for i in range(int(v["Children"])):
        agent_num += 1
        gender, age = select_children_ga(v, female_child_age, male_child_age, age_mom, i)
        agents[agent_num] = {"Family" : k,
                              "Tribe" : v["Tribe"], 
                              "House" : v["Structure"],
                              "Age": age, 
                              "Gender": gender,
                              "Employment": get_child_employment(v, age), 
                              "Water" : get_water(v),
                              "Electricity" : get_electricity(v), 
                              "RENT": get_rent(v), 
                              "Toilet" : get_toilet(v),
                              "Class": v["Class"]} 
                              
        
        
    return agents, agent_num
        




################################################
#
#  Main function 
#
#
##################################################

def make_agents(families): 
    
    print ("\n", "Beginning Phase III: Making agents\n" )
    
    women_age, men_age, female_child_age, male_child_age = make_age(families)
    
    '''
    child_array = []
    for k,v in families.items(): 
          
        if v["Children"] > 8:
            child_array.append(v["Children"])
        
    print (len(child_array))
    '''
        
    agents = {}
    
    agent_num = 0
        
    for k,v in families.items(): 
        #use logistic function to assign probability of age based on number of kids
        #do now to place husbands and wives near same age
        p_age = 1/(1+math.exp(-1*(v["Children"] -2)))
        p_elderly = random.randint(0,1)
        if v["Father"] == 1:
            agents, agent_num = make_male(k,v,men_age, agents, agent_num, p_age, p_elderly)
        if v["Mother"] > 0:
            agents, agent_num, age_mom = make_female(k,v,women_age, agents, agent_num, p_age, p_elderly)
        if v["Children"] > 0: 
            agents, agent_num = make_children(k,v, female_child_age, male_child_age, agents, agent_num, age_mom)
        
    print_demographics(women_age, men_age, female_child_age, male_child_age)
    print ("Number of Agents From Phase III: ", len(agents.keys()))
    
    print ("\nEconomic class by agent: ")
    build.print_agentclass(agents)
   
    
    return agents, female_child_age, male_child_age
        
    