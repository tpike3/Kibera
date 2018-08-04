# -*- coding: utf-8 -*-
"""
Created on Tue May  1 14:28:15 2018

Decison tress for Agents
"""

import update
import patternsoflife as pol
import purchase
import random
import math

def determine_requirements_calorie(member):
    
    '''
    Task: Determine Calorie need
    
    Process: Sum based on expended calories
    '''
    
    #print (member)
    calories = 0
    
    if member["Caloric"][1] < 0: 
            calories += (-1 * member["Caloric"][1]) + member["Caloric"][0]/3  # make sure turned positive for additional need
    else: 
        if (member["Caloric"][0]/3 - member["Caloric"][1]) > 0:     
            calories += member["Caloric"][0]/3 -  member["Caloric"][1]
        else: 
            pass

    return calories

def select_member(agent):
    '''
    Task: Select memeber to execute task
    
    Process: Prioritze adult females per the culture and then adult males
    then teenagers"
    '''    
    parent_list = ["18-25", "25-50", "51+"]
        
    if len(agent.members.keys()) == 1: 
        return agent.members.keys()[0]
    else: 
        possible = None
        
        for k,v in agent.members.items(): 
            if v["Age"] in parent_list and v["Gender"] == "F": 
                possible = k
            elif v["Age"] in parent_list and possible == None: 
                possible = k
            elif v["Age"] == "15-18" and possible == None:
                possible = k
        if possible == None: 
            print ("ONLY CHILDREN IN THE HOUSE")
        
        return k
    
def select_member_criminal(agent):
    
    '''
    Task: Select memeber to execute task
    
    Process: Prioritze adult males per the culture and then adult females
    then teenagers"
    '''    
    parent_list = ["18-25", "25-50", "51+"]
        
    if len(agent.members.keys()) == 1: 
        return agent.members.keys()[0]
    else: 
        possible = None
        
        for k,v in agent.members.items(): 
            if v["Age"] in parent_list and v["Gender"] == "M": 
                possible = k
            elif v["Age"] in parent_list and possible == None: 
                possible = k
            elif v["Age"] == "15-18" and possible == None:
                possible = k
        if possible == None: 
            print ("ONLY CHILDREN IN THE HOUSE")
        
        return k
    
        
def round_down(reqs):
    
    reqs2 = round(reqs, 2)
    
    if reqs2 > reqs:
        return (reqs2 - 100)
    else: 
        return reqs2


def check_resources(agent, reqs, shops, food_need):
    
    '''
    Task: Check to see if you have resources on hand to fulfill the need
    
    Process: Determine which resources are avialable and execute action
    '''    
    #print (agent.raw, len(agent.raw))
    #estimate cost based on simulated knoweldge of price
    shop = agent.raw[random.randint(0, len(agent.raw)-1)]
    price = shops[shop[0]].prices["pack_3"]
    #calculates cost for full buy
    cost = (reqs//100  * price) * 1.2 #account for continued calroie expenditure
    
        
    #round reqs avoid not eating based on a calorie or two
    reqs = round_down(reqs)
    
    
       
    if agent.resources["Food_cooked"] >= reqs: 
        return "full"
    #elif agent.resources['Food_cooked'] >= reqs * 0.8:
    #    return "partial"
    #check if agent has enough to cook --does not consider cooking partial meal
    elif agent.resources['Food_uncooked'] >= reqs: 
        return "cook"
    #if agent does not have food go buy food
    elif agent.resources["Wealth"] > cost: 
        return "buy food"
    #elif agent.resources["Food_cooked"] > len(agent.members) * 100:
    #    return "partial"
    else: 
        return "no resources"
            

def determine_need_night(physical, agent):
    
    sleep = [] 
    food = []
    water = []
    nothing = []
    
    
    for k,v in physical.items():
        if v["Sleep"] < 0.270 and v["Calories"] < 0.270 and v["Hydration"] < 0.270:
            nothing.append(k)
        elif v["Sleep"]*agent.members[k]["Bias"] >= v["Hydration"] and \
        v["Sleep"]*agent.members[k]["Bias"] >= v["Calories"]:
             sleep.append(k)
        elif v["Calories"] >= v["Hydration"] and v["Meal"] == False : # agent starving
             food.append(k)
        else: 
            #if meal action already taken default is sleep 
            sleep.append(k)

    return [sleep, food, water, nothing]

def determine_need_meal(physical, agent):
    
    sleep = [] 
    food = []
    water = []
    nothing = []
    social = []
    
    '''
    if agent.unique_id == 4242:
        print ("4242 Physical")
        print ("PHYSICAL", physical)
    '''
    
    for k,v in physical.items():
        #all needs meet
        if v["Sleep"] < 0.270 and v["Calories"] < 0.270 and v["Hydration"] < 0.270:
            nothing.append(k)
        #need sleep the most
        elif v["Sleep"] >= v["Hydration"] and v["Sleep"] *.7 > v["Calories"]:
             sleep.append(k)
        #need calories the most, but have not attempted to eat
        elif v["Calories"] >= v["Hydration"] and v["Meal"] == False : #############################  agent starving
             food.append(k)
        else: 
            #if meal action already taken socialize is default 
            social.append(k)

    return [sleep, food, water, nothing, social]


def school_meal(physical, agent):
    
    check = False
    
    for k,v in agent.members.items(): 
        if v["Employment"] == "Student":
            v["Caloric"][1] += v["Caloric"][2]
            agent.record["Eat"] += 1
            v["Meal"] = True
            check = True
    
    if check == True: 
        return pol.check_physical(agent.members)
    else: 
        return physical

def assess_child_labor(physical, agent):
    
    desperate = False
    
    if any(v["Calories"] > 0.89 for v in physical.values()):
        desperate = True
    
    
    if desperate == True:
        
        for k,v in agent.members.items():
            if v["Age"] == "10-14" and v["Employment"] == "Student":
                #print ("10-14 year old in family")
                v["Employment"] = "casual"
                agent.record["child_labor"] += 1
                break
                
    if desperate == False:
        for k,v in agent.members.items():
            if v["Age"] == "10-14" and v["Employment"] == "casual":
                #print ("10-14 year old in family")
                v["Employment"] = "Student"
                agent.record["child_labor"] -= 1
                break
        


#####################################################################
#
# REPEATED FUNCTIONS
#
####################################################################
    
def single_food_process(need_list, agent, visits, shops, criminal, physical, hour):
    
    """
    Task: Determine action to take for hunger
    
    Process: Determine requirements, resources, and state and 
    select an action
    """
    
    #determine requirements
    reqs = determine_requirements_calorie(agent.members[need_list[1][0]])
    #check your resources
    resources = check_resources(agent, reqs, shops, need_list[1])
    #choose an action 
    '''
    if agent.unique_id == 4242:
        print ("4242 Resources and Reqs")
        print (reqs, resources)
    '''
    #update meal status to True so agent will not try and get lots of meals (or skip lots)
    
    if resources == "full": 
        agent.members[need_list[1][0]]["Meal"] = True
        update.action_eat_full(need_list[1][0], agent, reqs)
    elif resources == "partial":
        agent.members[need_list[1][0]]["Meal"] = True
        update.action_eat_partial(need_list[1][0], agent, 1)
    elif resources == "cook":
        update.cook(need_list[1][0], agent, reqs)
    elif resources == "buy food":
        purchase.get_food(need_list[1][0], agent, reqs, visits, shops, hour, physical)
    elif resources == "no resources": 
        #if agent.resources["Wealth"] > 9: 
        #   purchase.get_food(need_list[1][0], agent, reqs, visits, shops, hour, physical)
        if physical[need_list[1][0]]["Calories"] > .95: 
            update.steal(need_list[1][0], agent, shops, criminal)
            agent.record["Steal"] += 1
        else: 
            agent.record["Skip Meal"] += 1
            agent.members[need_list[1][0]]["Meal"] = True
            #print (agent.members[need_list[1][0]])
            
            
def family_food_process(need_list, agent, visits, shops, criminal, physical, hour):

    reqs = 0
    req_list = {}
    
    '''
    if agent.unique_id == 319: 
        print ("FAMILY FOOD PROCESS CALLED")
    '''
   
    #determine total and individual need
    for mem in need_list[1]:
        #update meal status to True so agent will not try and get lots of meals (or skip lots)
        
        mem_req = determine_requirements_calorie(agent.members[mem])
        reqs += mem_req
        req_list[mem] = mem_req
        
    resources = check_resources(agent, reqs, shops, need_list[1])
       
    '''
    if agent.unique_id == 319: 
        print ("PART 2")
        print ("AGENT 319", reqs, resources)
    '''
    
    if resources == "full":
        #if resources available eat
        for mem in need_list[1]:
            agent.members[mem]["Meal"]= True
            update.action_eat_full(mem, agent, req_list[mem])
        for mem in need_list[0]:
            update.action_sleep(mem, agent)
        for mem in need_list[3]:
            agent.record["Needs Met"] += 1
            update.wait(mem, agent)
        if len(need_list) > 4:
            if len(need_list[4]) > 0:
                for mem in need_list[4]:
                    update.wait(mem, agent)
    #if some resources available 
    elif resources == "partial":
        #determine split based on percentage need of calories
        total = sum(req_list.values())
        for mem in need_list[1]:
            agent.members[mem]["Meal"]= True
            update.action_eat_partial(mem, agent, req_list[mem]/total)
        for mem in need_list[0]:
            update.action_sleep(mem, agent)
        for mem in need_list[3]:
            agent.record["Needs Met"] += 1
            update.wait(mem, agent)
        if len(need_list) > 4:
            if len(need_list[4]) > 0:
                for mem in need_list[4]:
                    update.wait(mem, agent)
                
    #if additional action required, select member
    elif resources == "cook": 
        member = select_member(agent)
        update.cook(member, agent, reqs)
        for mem in need_list[1]:
            if mem != member:
                update.wait(mem, agent)
        for mem in need_list[0]:
            if mem != member:
                update.action_sleep(mem, agent)
        for mem in need_list[3]:
            if mem != member:
                agent.record["Needs Met"] += 1
                update.wait(mem, agent)
        if len(need_list) > 4:
            if len(need_list[4]) > 0:
                for mem in need_list[4]:
                    if mem != member:
                        update.wait(mem, agent)
                    
    elif resources == "buy food": 
        member = select_member(agent)
        purchase.get_food(member, agent, reqs, visits, shops, hour, physical)
        mem_list = need_list[0] + need_list[1]
        for mem in mem_list: 
            if mem != member: 
                update.action_sleep(mem, agent)
        for mem in need_list[3]:
            if mem != member:
                agent.record["Needs Met"] += 1
                update.wait(mem, agent)
        if len(need_list) > 4:
            if len(need_list[4]) > 0:
                for mem in need_list[4]:
                    if mem != member:
                        update.wait(mem, agent)
    elif resources == "no resources":
        desperate = False
        min_sustain = False
        for mem in need_list[1]:
            if physical[mem]["Calories"] > .95:
                desperate = True
            elif agent.resources["Wealth"] > 9: 
                min_sustain = True
        '''
        if min_sustain == True: 
            member = select_member(agent)
            purchase.get_food(need_list[1][0], agent, reqs, visits, shops, hour,physical)
            mem_list = need_list[0] + need_list[1]
            for mem in mem_list: 
                if mem != member:
                    update.action_sleep(mem, agent)
            for mem in need_list[3]:
                agent.record["Needs Met"] += 1
                update.wait(mem, agent)
            if len(need_list) > 4:
                if len(need_list[4]) > 0:
                    for mem in need_list[4]:
                        update.wait(mem, agent) 
        '''                
        if desperate == True: 
            member = select_member_criminal(agent)
            update.steal(member, agent, shops, criminal)
            agent.record["Steal"] += 1
            mem_list = need_list[0] + need_list[1]
            for mem in mem_list: 
                if mem != member: 
                    update.action_sleep(mem, agent) 
            for mem in need_list[3]:
                agent.record["Needs Met"] += 1
                update.wait(mem, agent)
            if len(need_list) > 4:
                if len(need_list[4]) > 0:
                    for mem in need_list[4]:
                        if mem != member:
                            update.wait(mem, agent)
        elif desperate == False: # and min_sustain == False: 
            for member in need_list[1]:   
                agent.record["Skip Meal"] += 1
                agent.members[member]["Meal"] = True
                #print (agent.members[member])
            for mem in need_list[0]: 
                update.action_sleep(mem, agent)
            for mem in need_list[3]:
                agent.record["Needs Met"] += 1
                update.wait(mem, agent)
            if len(need_list) > 4:
                if len(need_list[4]) > 0:
                    for mem in need_list[4]:
                        update.wait(mem, agent)
                        


def non_work_single(physical, agent, hour, shops, visits, criminal):
    
    need_list = determine_need_meal(physical, agent)
    
    '''
    if agent.unique_id == 4242:
        print ("4242 NEED LIST- Non-work single")
        print (need_list)
    '''
    
    if len(need_list[0]) == 1:
        update.wait(need_list[0][0], agent)
        #update.action_sleep(need_list[0][0], agent)
    elif len(need_list[1]) == 1:
        single_food_process(need_list, agent, visits, shops, criminal, physical, hour)
    elif  len(need_list[3]) == 1: 
        agent.record["Needs Met"] += 1
        update.wait(need_list[3][0], agent)
    elif len(need_list[4]) == 1: 
        update.wait(need_list[4][0], agent)
    else:
        print ("Something is wrong - action; line 428")
        print (physical)
        print (agent)


def non_work_multi(physical, agent, hour, shops, visits, criminal):
    
    
    need_list = determine_need_meal(physical, agent)
    
    '''
    if agent.unique_id == 319:
        print ("NEED LIST")
        print (need_list)
    '''    
    if len(need_list[1]) > 0:
         family_food_process(need_list, agent, visits, shops, criminal,physical, hour)
                
    elif len(need_list[0]) > 0 or len(need_list[2]) > 0 or len(need_list[3]) > 0 or len(need_list[4]) > 0:
        for mem in need_list[0]:
            update.wait(mem, agent)
        for mem in need_list[3]:
            agent.record["Needs Met"] += 1
            update.wait(mem, agent)
        for mem in need_list[4]:
            update.wait(mem, agent)
    
    else:        
        print (need_list)
        print ("error in need list- actions 460")
        
    if hour == 19 and agent.poss_child == True: 
        #print ("CHild labor assessed")
        assess_child_labor(physical,agent)




#####################################################################
#
#
#    MAIN FUNCTION 
#
#
####################################################################




def select_action(physical, agent, hour, shops, visits, criminal, work_p):
    
    '''
    
    Task: Agent selects course of action
    
    Process: Time serves as coordination measure/ physical processes drive agent choices
    
    '''    
    ##################################################################
    #
    #  HOURS 2200 to 0500
    #
    ##################################################################
    
    
    if hour >= 22 or hour < 5:
        
        '''
        Task: Unless food or water need is severe, sleep
        
        Process: check needs and choose behavior, bias sleep during these hours
        '''       
        need_list = determine_need_night(physical, agent)
        
        #for single person families
        if len(agent.members.keys()) == 1: 
            
            #print (len(agent.members.keys()))
            #if only sleep needed sleep
            if len(need_list[0]) == 1: 
                update.action_sleep(need_list[0][0], agent)
            #if food most need, get food
            elif len(need_list[1]) > len(need_list[2]):
                #run decision tree for eating
                single_food_process(need_list, agent, visits, shops, criminal, physical, hour)
                    
            #if all needs met
            elif len(need_list[3]) ==1:
                agent.record["Needs Met"] += 1
                update.wait(need_list[3][0], agent)
            else: 
                print ("Something is wrong - action line 530")
                print (physical)
                print (agent)
               
        #for multi-person families            
        else: 
            '''
            Process: if there is a need, identify an action the family member needs to complete; member does action
            if travelling to store etc then everyone else sleeps, if cooking, hungry ones wait
            '''
                     
            #if all need sleep sleep
            if len(need_list[1]) == 0 and len(need_list[2]) == 0 and len(need_list[3])== 0: 
                for mem in need_list[0]:
                    update.action_sleep(mem, agent)
            
            #if someone needs something else
            elif len(need_list[1]) > 0: 
                
                family_food_process(need_list, agent, visits, shops, criminal,physical, hour)
            #To account for situation where all familiy is satsified and no one need anything 
            elif len(need_list[3]) > 0 and len(need_list[1]) == 0 and len(need_list[2]) == 0 and len(need_list[0]) == 0: 
                
                for mem in need_list[3]:
                    agent.record["Needs Met"] += 1
                    
            elif len(need_list[3]) > 0 and len(need_list[0]) > 0: 
                
                for mem in need_list[0]:
                    update.action_sleep(mem, agent)
                
                for mem in need_list[3]:
                    agent.record["Needs Met"] += 1
                
                    
            else: 
                print ("Something is wrong - action; line 530")
                print (need_list)
                print (physical)
        
        
    ###################################################################
    #
    #  HOURS 0500 to 0800
    #
    ##################################################################
    
    
    elif hour >=  5 and hour < 8: 
        
       
        
        if len(agent.members.keys()) == 1: 
                   
           non_work_single(physical, agent, hour, shops, visits, criminal)
                
        else: 
           non_work_multi(physical, agent, hour, shops, visits, criminal)
    
    ###################################################################
    #
    #  HOURS 0800 to 1200
    #
    ##################################################################                       
    
    
    elif hour >= 8 and hour < 12:
        
        #Process for work
        
        #if len(agent.members.keys()) == 1:
            
        for k,v in agent.members.items():
            update.work(k,v,agent, work_p, visits, hour)
            
    
    ###################################################################
    #
    #  HOURS 1200 to 1400
    #
    ##################################################################    
        
    elif hour >= 12 and hour < 15:
        
        if hour == 12:
            physical = school_meal(physical, agent)
               
        if len(agent.members.keys()) == 1:
            non_work_single(physical, agent, hour, shops, visits, criminal)
            
        else: 
            non_work_multi(physical, agent, hour, shops, visits, criminal)
            
    ####################################################################
    #
    #  HOURS 1400 to 1900
    #
    ####################################################################
    
    
    elif hour >=15 and hour < 19: 
      
        for k,v in agent.members.items():
            update.work(k,v,agent, work_p, visits, hour)     
            
    
    ##################################################################
    #
    # HOURS 1900 to 2200
    #
    ##################################################################
    
    elif hour >= 19 and hour < 22:
        
        
        
        if len(agent.members.keys()) == 1:
            non_work_single(physical, agent, hour, shops, visits, criminal)
            
        else: 
            non_work_multi(physical, agent, hour, shops, visits, criminal)
            #determine if child should work
            
        
        