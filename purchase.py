# -*- coding: utf-8 -*-
"""
Created on Sun May  6 12:47:09 2018

Purchase food

Tom Pike
CSS645
"""

import random

def select_food(f_member, req, agent, shop, type_food,physical):
    
    #determine number of 100 calories packages, add additional to account for calories burned during 
    # getting and cooking
    
    num_packs = (req//100 + len(agent.members.keys())*4) #additive factor to account for calories burned for intermittent time steps
        
    agent.record["Buy Food"] += 1
    
    #Account for deals
    
    if agent.resources["Wealth"] >= num_packs*shop.prices['pack_4']:
        num_packs = agent.resources["Wealth"] // shop.prices["pack_4"]
        #update actions for record
        agent.record['variety_4'] += 1 
        #update wealth
        agent.resources["Wealth"] -= num_packs*shop.prices['pack_4']
        agent.record["Food Cost"] += num_packs*shop.prices['pack_4']
        #update amount of calories in resources, consumed in next hour
        agent.resources[type_food] += num_packs*100
        #update amount of calories for family member who went to get food
        agent.members[f_member]["Caloric"][1] -= 30
    elif agent.resources["Wealth"] >= num_packs*shop.prices['pack_3']:
        num_packs = agent.resources["Wealth"] // shop.prices["pack_3"]
        #update actions for record
        agent.record['variety_3'] += 1 
        #update wealth
        agent.resources["Wealth"] -= num_packs*shop.prices['pack_3']
        agent.record["Food Cost"] += num_packs*shop.prices['pack_3']
        #update amount of calories in resources, consumed in next hour
        agent.resources[type_food] += num_packs*100
        #update amount of calories for family member who went to get food
        agent.members[f_member]["Caloric"][1] -= 30
    elif agent.resources["Wealth"] >= num_packs*shop.prices['pack_2']:
        num_packs = shop.prices["pack_2"]//agent.resources["Wealth"]
        #update actions for record
        agent.record['variety_2'] += 1 
        #update wealth
        agent.resources["Wealth"] -= num_packs*shop.prices['pack_2']
        agent.record["Food Cost"] += num_packs*shop.prices['pack_2']
        #update amount of calories in resources, consumed in next hour
        agent.resources[type_food]+= num_packs*100
        #update amount of calories for family member who went to get food
        agent.members[f_member]["Caloric"][1] -= 30
    else:
        pref_type = ["pack_2", "pack_3", "pack_4"]
        pref = random.randint(0,2)
        #buy what you can
        bought = agent.resources["Wealth"]//shop.prices[pref_type[pref]]
        agent.resources["Wealth"] -= shop.prices[pref_type[pref]] * bought
        agent.record["Food Cost"] += shop.prices[pref_type[pref]] * bought
        agent.resources[type_food] += 1 
        agent.record['variety_2'] += 1 #num_packs/len(agent.members.keys()) #bought
        agent.members[f_member]['Caloric'][1] -= 30
    

def cal_cost_benefit(f_member, agent, shops, reqs, store): 
    
    price_list = []
    
    
    if store == "24":
        shop_c = agent.cooked_24[0][0]
        shop_r = agent.raw_24[0][0]
    else:
        shop_c = agent.cooked[0][0]
        shop_r = agent.raw[0][0]
    
    #calculate most nutrients for price and req
    #create list of prices for variety based on needs 
    #data structure [(cook24pack2, raw24pack2), (cooked24pack3, raw24pack3), (cooked24pack4, raw24pack4)]   
    price_list.append(((reqs//100*shops[shop_c].prices["pack_4"])/agent.resources["Wealth"], \
                      ((reqs//100*shops[shop_r].prices["pack_4"])+shops[shop_r].prices["fuel"])/agent.resources["Wealth"] ))
    
    price_list.append(((reqs//100*shops[shop_c].prices["pack_3"])/agent.resources["Wealth"], \
                      ((reqs//100*shops[shop_r].prices["pack_3"])+shops[shop_r].prices["fuel"])/agent.resources["Wealth"] ))
    
    price_list.append(((reqs//100*shops[shop_c].prices["pack_2"])/agent.resources["Wealth"], \
                      ((reqs//100*shops[shop_r].prices["pack_2"])+shops[shop_r].prices["fuel"])/agent.resources["Wealth"] ))
          
    
    #iterate through list to get the best food with available resources
    for p in price_list: 
        if p[1] < 1 or p[0] < 1:
            if p[1] < p[0]:
                return "Food_uncooked", shop_r
            else:
                return "Food_cooked", shop_c
        else:
            pass
    
    #function dangler - not return before now for for cheapest to person variety
    if price_list[2][1] <price_list[2][0]:
        return "Food_uncooked", shop_r
    else:
        return "Food_cooked", shop_c
  

#########################################################
#
# MAIN FUNCTION 
#
########################################################


def get_food(member, agent, reqs, visits, shops, hour, physical): 
    
    if hour <=5 and hour >= 22: 
        choice, shop = cal_cost_benefit(member, agent, shops, reqs, "24")
        
    else: 
        choice, shop = cal_cost_benefit(member, agent, shops, reqs, "normal")
    
        
    visits[shop].append(member)
    select_food(member, reqs, agent, shops[shop], choice,physical)
                  

"""
def get_fuel_24(member, agent, visits):
    
    '''
    Task: Get fuel form nearest 24 hour shop
    
    Process: Check wealth for one/two and one meal increments and buy 
    available amount of fuel
    '''
    
    
    agent.record["Buy_Fuel"] += 1
    shop = agent.raw_24[0][0]
    visits[shop].append(member)
    #buy enough for 2 days if possible
    if agent.resources["Wealth"] > shop.fuel*6:
        agent.resources['Wealth'] -= shop.fuel *6
        agent.resources["Fuel"] += 6
    
    elif agent.resources["Wealth"] > shop.fuel * 3:
        agent.resources["Wealth"] -= shop.fuel * 3
        agent.resources["Fuel"] += 3
        
    else: 
        agent.resources["Wealth"] -= shop.fuel
        agent.resources["Fuel"] += 1
 """           