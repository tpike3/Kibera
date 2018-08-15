
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 05:36:29 2018
Tom Pike
CSS645
Kianda Slum Population During Riots
Run Module
"""

from Main import *
import multiruns as mr

model_runs = {}

runs = mr.runs()

i = 1
z = 1
num_hrs = 2016 #1 week = 168 hours


for r in runs:
    for x in range(z):
        print ("Model run ", i , " of ", len(list(mr.runs()))*z)
        print ("Number of Days = ", num_hrs/24)
        test = Main(r[0],r[1]) # input parameter sets initial wealth; divisor for monthly rent, multiplier of daily rent for pay; probability of work.
        #run for 1 week- 168 hours
        for l in range(num_hrs):
                test.step()
        model_runs[(i,r[0],r[1])] = test.dataout
        i += 1
    
    
    
print ("MODEL RUNS")
#print (model_runs)
mr.exportdata(model_runs)    
    

'''
family_size = [len(a.members.keys()) for a in test.schedule.agents]
plt.close()
plt.hist(family_size)
plt.show()
'''


