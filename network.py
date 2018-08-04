# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 05:30:10 2018

Create network

Tom Pike
CSS645
"""

import networkx as nx

###############################################
#
# HELPER FUNCTIONS
#
#
##############################################

def add_agents(agents,G): 
    
    for k,v in agents.items(): 
        G.add_node(k)
        
    print (len(list(G.nodes)))
        
    
    
    return agents, G






#################################################
#
#
# MAIN FUNCTION 
#
#
###################################################


def make_network(agents):
    
    G = nx.Graph()
    agents, G = add_agents(agents, G)
    