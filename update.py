# -*- coding: utf-8 -*-
"""
Created on Wed May  2 05:16:12 2018

@author: ymamo
"""
#import movement
import purchase
import random


def action_sleep(f_member, agent):
    
    '''
    Task: Update sleep
    
    Process:  Update sleep value of each member, reduce calories, rcord action
    '''
    #take action
    agent.members[f_member]['Sleep'][1] += 1
    #update calories situation
    agent.members[f_member]["Caloric"][1] -= (agent.members[f_member]["Caloric"][0])/24
    #agent.members[f_member]["Hydration"][1] -= agent.members[f_member]["Hydration"][0]/24   
    #record action
    agent.record["Sleep"] += 1
        
    
def action_eat_full(f_member, agent, reqs):
    
    '''
    Task: Eat full meal
    Process: update attributes
    '''
    #account for earlier rounding to eat only what is on hand vs what is needed 
    if reqs > agent.resources["Food_cooked"]: 
        reqs = agent.resources["Food_cooked"]
    
    '''
    if agent.unique_id == 4242: 
        print ("4242 EATING")
        print (agent.members[f_member]["Caloric"], agent.resources["Food_cooked"]  )
    '''
    #check if agent has enough food for full meal
    agent.members[f_member]["Caloric"][1] += reqs
    agent.members[f_member]["Sleep"][1] -= agent.members[f_member]["Sleep"][2]
    agent.record["Eat"] += 1
    agent.resources["Food_cooked"] -= reqs
    
    if agent.resources["Food_cooked"] < -1: 
        print (agent.unique_id, reqs, agent.resources["Food_cooked"])
    
    '''
    if agent.unique_id == 4242: 
    
        print (agent.members[f_member]["Caloric"], agent.resources["Food_cooked"]  )
    '''
    
def action_eat_partial(f_member, agent, alotted):

    '''
    Task: Eat a partial meal
    
    Process: update attributes
    '''    
    agent.members[f_member]["Caloric"][1] += agent.resources["Food_cooked"]*alotted
    agent.members[f_member]["Sleep"][1] -= agent.members[f_member]["Sleep"][2]
    agent.resources["Food_cooked"] -= agent.resources["Food_cooked"]*alotted
    agent.record["Partial Eat"] += 1

def cook(member, agent, reqs): 
    """
    Task: Cook raw food
    
    Process: Cooker burns calories and family food gets updated
    """
    '''
    if agent.unique_id == 4242: 
        print ("agent 4242")
        print (agent.resources["Food_cooked"],agent.resources["Food_uncooked"] )
    '''
    agent.members[member]["Caloric"][1] -= agent.members[member]["Caloric"][2] * (1.2)
    agent.resources["Food_cooked"] += agent.resources["Food_uncooked"]
    agent.resources["Food_uncooked"] -= agent.resources["Food_uncooked"]
    agent.record["Cook"] += 1
    
    '''
    if agent.unique_id == 4242: 
        print ("agent 4242")
        print (agent.resources["Food_cooked"],agent.resources["Food_uncooked"] )
    '''
        
def wait(member, agent):
    """
    Task: Agents socialize
    
    Process: Burn calories record socail engagement
    """
    
    agent.members[member]["Caloric"][1] -= agent.members[member]["Caloric"][2] * (1+ random.random())
    agent.members[member]["Sleep"][1] -= agent.members[member]["Sleep"][2]
    agent.record["Social"] += 1
    
def steal(member, agent, shops, criminal):
    """
    Task: Agents Steals Food
    
    Process: Selects and type and shop at random to rob from, burn calories 
    has a 50-50 chance of success
    """
    
    
    #record action 
    agent.record["Steal"] += 1
    #determine area to steal from 
    shop_type = random.randint(1,4)
    if shop_type == 1: 
        shop = agent.cooked[random.randint(0, 12)]
    elif shop_type == 2: 
        shop = agent.cooked_24[random.randint(0,9)]
    elif shop_type ==3: 
        #print (agent.raw)
        shop = agent.raw[random.randint(0,19)]
    elif shop_type == 4: 
        #print (agent.raw_24)
        shop = agent.raw_24[random.randint(0,4)]
    
    #append to list
    criminal[shop[0]].append(member)
    #determine probability
    chance = random.random() + agent.record["Steal"]/100 # accounts for experience
    
    if chance < 0.5:
        agent.members[member]["Caloric"][1] -= agent.members[member]["Caloric"][2] * (1+ random.random())
        agent.members[member]["Sleep"][1] -= agent.members[member]["Sleep"][2] 
    else: 
        agent.members[member]["Caloric"] -= agent.members[member]["Caloric"][2] * (1+ random.random())
        agent.members[member]["Sleep"][1] -= agent.members[member]["Sleep"][2]
        #if chance < 0.33: 
        agent.resources["Wealth"] += shops[shop[0]].prices["pack_2"]*random.randint(1,4)
        #elif chance >= 0.33 and chance < 0.67: 
        #    agent.resources["Wealth"] += shops[shop[0]].prices["pack_3"]*random.randint(1,4)
        #else: 
        #     agent.resources["Wealth"] += shops[shop[0]].prices["pack_4"]*random.randint(1,4)
        
def work(k,v,agent, work_p, visits, hour):
    
    
    #initial set
    if v["Work"] == '':
        if v["Employment"] == "regular" or v["Employment"] == "fixed" or v["Employment"] == "B_Owners" \
        or v["Employment"] == "other" or v["Employment"] == "B_Owner":
            v["Work"] = "Work"
            agent.resources["Wealth"] += agent.pay
            agent.record["Work"] += 1
            work_f = random.randint(1,2) + random.random()
            agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] * work_f
            agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2] 
            
        elif v["Employment"] == "Student":
            v["Work"] = "Student"
            agent.record["Educate"] += 1
            agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] * 1.2
            agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2] 
            
        elif v["Employment"] == "casual" or (v["Employment"] == "unemployed" and agent.requirements["Nurturing"] == 0):
            
            #add agent to log to build out network
            shop = agent.job_locs[random.randint(0,len(agent.job_locs)-1)]
            visits[shop[0]].append(k)
            
            if random.random() <= work_p:
               v["Work"] = "Work"
               agent.resources["Wealth"] += agent.pay
               agent.record["Work"] += 1
               work_f =  random.randint(1,2) + random.random()
               agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] * work_f  
               agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2] 
            else: 
               v["Work"] = "Looking"
               agent.record["Look for Work"] += 1
               agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] * 1.2
               agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2] 
                        
        elif v["Employment"] == "unemployed" and agent.requirements["Nurturing"] > 0:
            
            age_list1 = ["18-25", "25-50", "51+"]
            age_list2 = ["10-14", "15-18"]
            possibles = 0
            nurturer = ""
            for k,v in agent.members.items():
                if v["Age"] in age_list1 and v["Gender"] == "F" and nurturer =="":
                    v["Work"] = "Nurture"
                    nurturer = "mother"
                if (v["Age"] in age_list1 or v["Age"] in age_list2) and v["Gender"] == "F":
                    possibles += 1
                
            if nurturer == "" and possibles > 0:
                for k,v in agent.members.items():
                    if v["Age"] in age_list2 and v["Gender"] == "F":
                        v["Work"] = "Nurture"
                        nurturer = "sister"
            if nurturer == "" and possibles == 0: 
                v["Work"] = v["Work"]
                agent.record["Child Danger"] += 1
                if random.random() <= work_p:
                    v["Work"] = "Work"
                    agent.resources["Wealth"] += agent.pay
                    agent.record["Work"] += 1
                    work_f = random.randint(1,2) + random.random()
                    agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] * work_f
                    agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2] 
                else: 
                   v["Work"] = "Looking"
                   agent.record["Look for Work"] += 1
                   agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] *1.2
                   agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2]  
                
            agent.record["Nurture"] += 1
            try: 
                agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] * 1.2
            except: 
                print (agent.members[k]["Caloric"][1])
                print (agent.members[k]["Caloric"][2])
            agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2] 
        
        elif v["Employment"] == "Too young":
            v["Work"] = "Too young"
            agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] 
            agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2]
                            
        else:
            print ("Agent Does not have a role updates-line 163")
            print (agent.members)
            #pass
   
    else: 
        if v["Work"] == "Work":
            agent.record["Work"] += 1 
            work_f =  random.randint(1,2) + random.random()
            agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] *work_f
            agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2] 
        elif v["Work"] == "Student":
            agent.record["Educate"] += 1
            agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] * 1.2
            agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2]
        elif v["Work"] == "Nurture":
            agent.record["Nurture"] += 1
            agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] * 1.5
            agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2] 
            agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2]
            agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2]
        elif v["Work"] == "Looking":
            if hour < 12 and random.random() <= work_p:
               v["Work"] = "Work"
               agent.record["Work"] += 1
               agent.resources["Wealth"] += agent.pay
               work_f =  random.randint(1,2) + random.random()
               agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] * work_f
               agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2]  
            else: 
               agent.record["Look for Work"] += 1
               agent.members[k]["Caloric"][1] -= agent.members[k]["Caloric"][2] * 1.4
               agent.members[k]["Sleep"][1] -= agent.members[k]["Sleep"][2] 
        
        
                    
                
        

            