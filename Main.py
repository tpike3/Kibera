# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 05:15:42 2018
Tom Pike
CSS645
Kianda Slum Population During Riots
Main Module
"""



from mesa import Model
#from time_adj import RandomActivationwGroups
from mesa.time import RandomActivation
import slum_graph as SG
import visualization 
import SlumAgent as SA
import record
import numpy as np
import warnings
import pickle
#from families import make_families

class Main(Model):
    
    def __init__(self, p_wealth, work_p):
        
        self.work_p = work_p
        self.hour = 5
        self.day = 1
        self.shops = self.load_obj("shops.pkl")
        self.children = self.load_obj("children.pkl")
        self.pop_size = self.load_obj("pop_size.pkl")
        #used to stop overflow warnings--nonlinear equations cause numbers to have too many numbers
        warnings.filterwarnings("ignore")
        
        ###############################################################
        #
        #  Add agents to schedule
        #
        ###############################################################
        #Read in families
        self.families = self.load_obj("population.pkl")
        self.num_families = len(self.families.keys())
        self.schedule = RandomActivation(self)
        for k,v in self.families.items(): 
           agent = SA.SlumAgent(self, k,v, p_wealth) 
           self.schedule.add(agent)
        
        ################################################################
        #
        # RECORDS
        #
        ###############################################################       
        
        self.visits = self.create_visit_log()
        self.criminal = self.create_visit_log()
        self.dataout = {}
        self.meals = {"3 Meals" : 0, "2 Meals" : 0, "1 Meal": 0, "0 Meals" : 0, "3+ Meals": 0} #}, "3_partial" : 0,"2_partial":0, "1_partial":0 }
        self.variety = {"4 Food Types":0, "3 Food Types":0, "2 Food Types":0}
        self.child_labor = 0
        self.meal_cost = 0 
        self.meal_distro = []
        self.steal = 0
        self.partial = 0
        self.wealth_distro = []
        self.total_child = {}
        
        
                
        print ("\nBEGIN MODEL" )
        print ("Parameters: ", p_wealth," ", work_p)
        
    ###########################################################################
    #
    #    Init HELPER FUNCTIONS
    #
    ###########################################################################
    
    # Load in syntetic population 
    def load_obj(self, name):
        with open( "./Population/" + name , 'rb') as f:
            return pickle.load(f)
            
    def create_visit_log(self):
        
        visit_log = {}
        
        for k in self.shops.keys(): 
            visit_log[k] = []
            
        return visit_log
    
    
            
        
    
    ###########################################################################
    #
    #     Data Management Functions
    #
    ###########################################################################
    
    def data_reset(self):
        
        self.meals = {"3 Meals" : 0, "2 Meals" : 0, "1 Meal": 0, "0 Meals" : 0, "3+ Meals" : 0 } #}, "3_partial" : 0,"2_partial":0, "1_partial":0 }
        self.variety = {"4 Food Types":0, "3 Food Types":0, "2 Food Types":0}
        self.child_labor = 0
        self.meal_cost = 0 
        self.meal_total = 0
        self.steal = 0
        self.partial = 0
        self.meal_distro = []
        self.wealth_distro = []
        
        for agent in self.schedule.agents:
            
            agent.record["Eat"] = 0
            agent.record["Skip Meal"] = 0
            agent.record["variety_4"] = 0
            agent.record["variety_3"] = 0
            agent.record["variety_2"] = 0
            agent.record["Food Cost"] = 0
            agent.record["Steal"] = 0
            agent.record["Partial"] = 0
            agent.record["child_labor"] = 0
    
    
    
    
    def update_stats(self):
        
        child_labor = 0
        meal_cost = 0
        #print ("Child Labor")
        #print (len(self.total_child.keys()), sum(self.total_child.values()), self.children)
      
        for agent in self.schedule.agents:
            
            #markerfam = False
            '''
            if agent.unique_id ==4242: 
                print ("")
                print ("Agent 5966: Family Size =  ", len(agent.members))
                print (agent.requirements)
                print (agent.record)
                print (agent.resources)
                print (agent.members)
                print ("")
            '''        
            #Gather Meals Data
            num_full = int(agent.record["Eat"])
            num_partial = int(agent.record["Partial Eat"])
            #num_skips = int(agent.record["Skip Meal"])
            num_fam = len(agent.members.keys())
            self.partial += num_partial
            self.steal += int(agent.record["Steal"])            
            #if (num_fam ==  5 and "0-4" in agent.members.values()) or num_fam==5: 
            #    markerfam = True
            a_meals = num_full + num_partial
            
            #Calculate number of meals eaten per person
            meal_list = [0,0,0,0,0]
            num_meals = a_meals // num_fam
            #print (num_meals)
            rem = a_meals % num_fam
            if num_meals == 2: 
                meal_list[1] = num_fam
                while rem > 0:
                    meal_list[1] -= 1
                    meal_list[0] += 1
                    rem -= 1
            elif num_meals >= 3 and rem >=0:
                meal_list[0] = num_fam
                #while rem > 0: 
                #    meal_list[4] += 1
                #    meal_list[0] -= 1
            elif num_meals == 1: 
                meal_list[2] = num_fam
                while rem > 0: 
                    meal_list[1] += 1
                    meal_list[2] -= 1
                    rem -= 1
            elif num_meals == 0: 
                meal_list[3] = num_fam
                while rem > 0: 
                    meal_list[2] += 1
                    meal_list[3] -= 1
                    rem -= 1
            else: 
                print ("error in meal calc")
                     
                        
            self.meals["3 Meals"] += meal_list[0]
            self.meals["2 Meals"] += meal_list[1]
            self.meals["1 Meal"] += meal_list[2]
            self.meals["0 Meals"] += meal_list[3]
            
            #Gather Variety Data
            self.variety["4 Food Types"] += agent.record["variety_4"]
            self.variety["3 Food Types"] += agent.record["variety_3"]
            self.variety["2 Food Types"] += agent.record["variety_2"]
            
            
            #Gather Child Labor Data
            
            
            if agent.record["child_labor"] > 0:
                
                child_labor += agent.record["child_labor"]
                if agent.unique_id not in self.total_child.keys(): 
                    self.total_child[agent.unique_id] = agent.record["child_labor"]
                else: 
                    if agent.record["child_labor"] > self.total_child[agent.unique_id]:
                        self.total_child[agent.unique_id] = agent.record["child_labor"]
            
            #Gather Meal Cost Data
            
            meal_cost += agent.record["Food Cost"]/num_fam
            
            #if markerfam == True: 
            self.meal_distro.append([agent.unique_id, agent.record["Food Cost"], num_fam, agent.requirements["Caloric"]])
            self.wealth_distro.append([agent.unique_id, agent.resources["Wealth"]])
            
            
       
        self.child_labor2 = sum(self.total_child.values())/self.children
        self.child_labor = child_labor/self.children
        self.meal_cost = meal_cost/self.num_families
        
        
        
        #Store data for day
        self.dataout[self.day] = [self.meals, self.variety, self.child_labor, self.meal_cost, \
                                self.wealth_distro, self.steal, self.meal_distro, self.child_labor2]
        
        #Reset Data
        self.data_reset()
                   
    def time_update(self):
        
        if self.hour == 24: 
            self.hour = 0
            self.day += 1
        else: 
            self.hour += 1
            
    
    
    def time_sync(self):
        
        if self.hour == 22 or self.hour == 5 or self.hour == 12 \
            or self.hour == 19:
            
            if self.hour == 22: 
                for agent in self.schedule.agents:
                    for v in agent.members.values():
                        v["Meal"] = False
                        v["Work"] = ""
                                
                self.update_stats()
                
                print ("\nDay ", self.day, " Complete.")
    
            else: 
                for agent in self.schedule.agents:
                    for v in agent.members.values():
                        v["Meal"] = False
    
    ############################################################################
    #
    #      STEP FUNCTION 
    #
    #############################################################################
    
    
    def step(self):
        '''Advance the model by one step.'''
        #Keep track of time
        #print ("\nDay: ", self.schedule.day )
        #print("   Hour: ", self.schedule.hour)
        # Reset Meal and Work Status
        self.time_update()
        self.time_sync()    
        self.schedule.step()  
       
        
        