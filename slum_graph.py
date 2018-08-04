# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 05:30:10 2018

Create network

Tom Pike
CSS645
"""

import networkx as nx
import itertools

###############################################
#
# HELPER FUNCTIONS
#
#
##############################################

def add_agents(agents,G): 
    
    ##########################################
    #
    # Task: Takes each agent and places them in a node in the graph
    #
    # Process: Add agent number as node; 
    #set attributes to dictionary of agent attributes
    #
    ##################################################
    
    for k,v in agents.items(): 
        G.add_node(k)
    nx.set_node_attributes(G, agents)
       
        
    return G


def make_linkDicts(agents):
    
    ############################################
    #
    #Task: create dictionary for easy link creation
    #
    #Process: for loop with dictionary creation
    #
    ###################################################
    
    fam_dict = {}
    house_dict = {}
    
    #place agent in family dictionary
    # structure key = family number, 
    #value = list of family members by agent number 
    for k, v in agents.items(): 
        if v["Family"] not in fam_dict.keys(): 
            fam_dict[v["Family"]] = [k]
        else: 
            fam_dict[v["Family"]].append(k)
    
        #place agents in house dictionary 
        #structure key = house id
        #value = list of agents
        if v["House"] in house_dict.keys():  
            house_dict[v["House"]].append(k)
        else: 
            house_dict[v["House"]] = [k]
    
          
    return fam_dict, house_dict


def link_family(G, fam_dict):
    
    ###################################################
    #
    # Task: Link family members with weight one to share resources
    #
    # Process: Use native networkx processes
    #
    #################################################
    
    
    for v in fam_dict.values(): 
        if len(v) > 1: 
            combinations = itertools.combinations(v,2)
            G.add_edges_from(combinations, weight=1)
            #print (combinations)
                       
    return G

def link_house(G, house_dict):
    
    ######################################################
    #
    # Task: Link agents with weight 0.25, can hep each other
    # future iterations need a more ocmpex weight structure
    #
    #Process: Use native networkx processes; skip if family member
    #
    ########################################################
    
    for k,v, in house_dict.items():
        if len(v) > 1: 
            combinations = itertools.combinations(v,2)
            for c in combinations: 
                #skip if link already there due to family member
                if G.has_edge(*c[:2]):
                    pass
                else: 
                    G.add_edge(*c, weight = 0.25)                ##############possible tuning parameter

    return G
#################################################
#
#
# MAIN FUNCTION 
#
#
###################################################


def make_network(agents):
    
    print (("\nPhase V: Your population is networked: \n" ))
    
    G = nx.Graph()
    G = add_agents(agents, G)
    fam_dict, house_dict = make_linkDicts(agents)
    G = link_family(G, fam_dict)
    G = link_house(G, house_dict)
    
    print ("Population Linked: " )
    print ("There are ", G.number_of_nodes(), " nodes.")
    print ("There are ", G.number_of_edges(), " edges.")
        
    return agents, G, fam_dict