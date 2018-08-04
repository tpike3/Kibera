# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 05:15:42 2018
Tom Pike
CSS645
Kianda Slum Population During Riots
Main Module
"""



import dbfRead as read_data
from simpledbf import Dbf5
import build as build
import agentize
import jobs
import phenotypes
import familyAgents
import movement
import pandas as pd
import pickle

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
def children_total(females,males):
        return females["10-14"][1]+males["10-14"][1]


###############################################################
#
# Get data and make dictionaries for agent creation
#
#############################################################

#Read in data
filename = "C:\\Users\\ymamo\\Kibera\\KIANDA_shapefile\\KIANDA_STRUCTURES\\Population_2\\kianda_structures_and_population_dataset.dbf"

dbf = Dbf5(filename)
df = dbf.to_dataframe()
#turn data into liked agent network - phasea listed correspond with printout
#Phase 1
pop_dict, business_dict, owner_dict, infra_dict = read_data.get_Agents_Phase1(df)
#Phase 2
initial_families = build.agents_Phase2(pop_dict,business_dict, owner_dict, infra_dict)
#Phase 3
pop,female_child_age,male_child_age = agentize.make_agents(initial_families)
#Phase 4
pop = jobs.make_jobs(pop)
pop = phenotypes.make_phenotypes(pop)
pop_size = len(pop.keys())
gis = movement.Movement()
shops = gis.shops()
families, services, water = familyAgents.make_families(pop, gis, shops)
children = children_total(female_child_age,male_child_age)


#Save data necessary for use in model
save_obj(families, "population" )
save_obj(shops, "shops")
save_obj(children, "children")
save_obj(pop_size, "pop_size")
#save_obj(water, "water")

#saved for reference
populations = pd.DataFrame(families)        
populations.to_csv("Kianda_Pop.csv")


    

        