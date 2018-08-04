# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 05:26:31 2018
Tom Pike
CSS645
Kianda Slum Population During Riots
Main Module
"""

from mesa import Agent
import patternsoflife as pol


class SlumAgent(Agent):
    
    def __init__(self, model, unique_id, v, p_wealth):
        super().__init__(unique_id, model)
        
        self.requirements = v["Requirements"] #contains calorie, hydration, nurturing, and rent
        self.members = v["Members"] #dictionary with k = agent number, values = Age, Employment, Gender, Sleep
        self.resources = v["Resources"] #consumable resources wealth, food, oil, electricity, house, water, toilet
        self.tribe = v["Tribe"]
        self.record = v["Actions"] #list of tasks based associated with 3 categories of Maslow's heirarchy of needs (physical, security and social)
        self.cooked = v["B_cooked"]
        self.cooked_24 = v["B_24_cooked"]
        self.raw = v["B_raw"]
        self.raw_24 = v["B_24_raw"]
        self.job_locs = v["B_jobs"]
        self.water = v["Water_points"]
        self.pay = (v["Requirements"]["Rent"]/30)*p_wealth
        self.poss_child = self.poss_labor(self.members)
        
    def poss_labor(self, members):
        
        cl = False
        
        for k,v in self.members.items(): 
            if v["Age"] == "10-14":
                cl = True
                break
        
        return cl
    
    def step(self):
        pol.complete_tasks(self, self.model.hour, self.model.shops,\
                           self.model.visits, self.model.criminal, self.model.work_p)