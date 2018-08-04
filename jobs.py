# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 15:33:00 2018

From a dictionary of agents

Assign vectors of tasks/specializations/behavior

Tom Pike
CSS645
"""


import random 


####################################################
#
# HELPER FUNCTIONS
#
##################################################

def create_job_dict(agents, employed_ages): 
    
    ##################################
    #
    # Task: Create dictionary to assign jobs
    #
    #
    # Process: get total number of employed
    # assign number of jobs based on 
    # Kenya Inside Informality: Poverty, Jobs, Housing and Services in Nairobi's Slum (Gulyani 2006)
    #
    # Child labor numbers based on 
    # Annabel S. Erulkar and James K. Matheka,
    #“Adolescence in the Kibera Slums of Nairobi, Kenya,” 2007, 28
    #
    ############################################
    
    
    jobs_m = 0
    jobs_f = 0
    child_male = 0
    child_female = 0
    
    #get adult jobs employment; child numbers for labor statistics
    for v in agents.values(): 
        if v["Age"] in employed_ages and v["Employment"] == "TBD": 
            if v["Gender"] == "M": 
                jobs_m += 1
            else: 
                jobs_f += 1
                
        if v["Age"] == "10-14": 
            if v["Gender"] == "F":
                child_female += 1
            else: 
                child_male += 1
    
    # Jobs type
    jobs_dict_m = {"unemployed" : [int(jobs_m *0.12),0], "regular" : [int(jobs_m *0.41),0], 
                "casual" : [int(jobs_m *0.41), 0], "student" : [int(jobs_m*.05),0], 
                "fixed" : [int(jobs_m * 0.01),0], "other": [int(jobs_m*.01),0],
                "child_labor_M": [int(child_male * 0.23), 0], 
                "children_not_employed": 0,
                "B_Owners" : 0
                }
    
    jobs_dict_f = {"unemployed" : [int(jobs_f *0.62),0], "regular" : [int(jobs_f *0.15),0], 
                "casual" : [int(jobs_f *.15), 0], "student" : [int(jobs_f*.07),0], 
                "fixed" : [int(jobs_f * 0.01),0], "other": [int(jobs_f *0.01),0],
                "child_labor_F": [int(child_female * 0.14), 0], 
                "children_not_employed": 0,
                "B_Owners" : 0
                }
    
    #print ("JOBS: Male: ", jobs_dict_m)
    #print ("JOBS: female: ", jobs_dict_f)
    
    return agents, jobs_dict_m, jobs_dict_f   



        
        


def assign_jobs(agents, jobs_dict_m, jobs_dict_f, employed_ages): 
    
    #######################################################################
    #
    # Task: Assign job 
    #
    #Process: Assumption is high rent means person is able to afford
    #so they get prioiry for jobs; families who are poor have children 
    #who needed to work earlier
    #
    ###############################################################
    family_list = []
    
    
    for v in agents.values(): 
        if v["Employment"] != "TBD": # or v["Employment"] == "Too young": 
            if v["Employment"] == "Too young":
                if v["Gender"] == "M":
                    jobs_dict_m["children_not_employed"] += 1
                else: 
                    jobs_dict_f["children_not_employed"] += 1
            else: 
                if v["Gender"] == "M": 
                    jobs_dict_m["B_Owners"] += 1
                else: 
                    jobs_dict_f["B_Owners"] += 1
    
    
    #Assign male employment
    for v in agents.values():             
        
        if v["Employment"] == "TBD" and v["Gender"] == "M": 
            
            #Assign male adult employment 51+
            if v["Age"] == employed_ages[-1]: 
                if v["Class"] == "Middle" or v["Class"] == "Upper":
                    v["Employment"] = 'fixed'
                    jobs_dict_m["fixed"][1] += 1    
                    
                else: 
                    if jobs_dict_m["other"][1]  < jobs_dict_m["other"][0]: 
                        v["Employment"] = 'other'
                        jobs_dict_m["other"][1] += 1
                    else: 
                        v["Employment"] = 'fixed'
                        jobs_dict_m["fixed"][1] += 1
        
            #Assign male adult employment over 18 - 50
            elif v["Age"] in employed_ages[1:3]: 
                if v["Class"] == "Upper" and jobs_dict_m["regular"][1]  <= jobs_dict_m["regular"][0]: 
                    v["Employment"] = "regular"
                    jobs_dict_m['regular'][1] += 1
                    #keep track of family to assign spouse to unemployed (i.e. stay at home mother)
                    family_list.append(v["Family"]) 
                elif v["Class"]== "Middle" and jobs_dict_m["regular"][1]  <= jobs_dict_m["regular"][0]:
                    v["Employment"] = "regular"
                    jobs_dict_m['regular'][1] += 1
                    family_list.append(v["Family"])
                elif v["Class"]== "Middle" and jobs_dict_m["casual"][1]  <= jobs_dict_m["casual"][0]:
                    jobs_dict_m['casual'][1] += 1
                    family_list.append(v["Family"])
                elif v["Class"] == "Lower":
                    if random.random() < 0.5 and jobs_dict_m["casual"][1]  <= jobs_dict_m["casual"][0]:
                        v["Employment"] = "casual"
                        jobs_dict_m["casual"][1] += 1
                    else: 
                        if jobs_dict_m["unemployed"][1]  <= jobs_dict_m["unemployed"][0]: 
                            v["Employment"] = "unemployed" 
                            jobs_dict_m["unemployed"][1] += 1
                        elif jobs_dict_m["casual"][1]  <= jobs_dict_m["casual"][0]: 
                            v["Employment"] = "casual" 
                            jobs_dict_m["casual"][1] += 1
                        elif jobs_dict_m["regular"][1]  <= jobs_dict_m["regular"][0]: 
                            v["Employment"] = "regular" 
                            jobs_dict_m["regular"][1] += 1
            
            #assigned 15-18
            #assign student status to upper class
            elif v["Age"] == employed_ages[0]: 
                if (v["Class"] == "Middle" or v["Class"] == "Upper") and v["Family"] in family_list \
                and jobs_dict_m["student"][1]  < jobs_dict_m["student"][0]: 
                    v["Employment"] = "Student"
                    jobs_dict_m["student"][1] += 1
                elif jobs_dict_m["casual"][1]  < jobs_dict_m["casual"][0]:
                    v["Employment"] = "casual"
                    jobs_dict_m["casual"][1] += 1
                elif jobs_dict_m["regular"][1]  < jobs_dict_m["regular"][0]:
                    v["Employment"] = "regular" 
                    jobs_dict_m["regular"][1] += 1
            
            elif v["Age"] in employed_ages: 
                    print ("Error assigning employment")
                                
                
    
        #Assign female adult employment over 15 1st go
        if v["Employment"] == "TBD" and v["Gender"] == "F": 
            
            
            if v["Age"] in employed_ages[-1]: 
                if (v["Class"] == "Middle" or v["Class"] == "Upper") and \
                jobs_dict_f["fixed"][1]  < jobs_dict_f["fixed"][0] : 
                    v["Employment"] = "fixed"
                    jobs_dict_f["fixed"][1] += 1
                else: 
                    if jobs_dict_f["other"][1]  < jobs_dict_f["other"][0]: 
                        v["Employment"] = "other"
                        jobs_dict_f["other"][1] += 1
                    else: 
                        v["Employment"] = "fixed"
                        jobs_dict_f["fixed"][1] += 1
            
            elif "Children" in v: 
                if v["Family"] in family_list and v["Age"] in employed_ages and v["Children"] > 0: 
                    if v["Class"] == "Upper" or v["Class"] == "Middle":
                        v["Employment"] = "unemployed"
                        jobs_dict_f["unemployed"][1] += 1 
            
            #Assign female middle class
            elif v["Age"] in employed_ages[1:3]:  
                if v["Class"] == "Middle" or v["Class"] == "Upper": 
                    v["Employment"] = "regular"
                    jobs_dict_f["regular"][1] += 1
                    
            elif v["Age"] in employed_ages[0]:
                if v["Class"] == "Upper": 
                    v["Employment"] = "Student"
                    jobs_dict_f["student"][1] += 1
                    
            
    #assign females over 15 second go            
    for v in agents.values(): 
        if v["Employment"] == "TBD" and v["Gender"] == "F": 
            if v["Age"] in employed_ages[1:3]: 
             if random.random() < 0.5 and jobs_dict_f["regular"][1]  < jobs_dict_f["regular"][0]: 
                 v["Employment"] = "regular"
                 jobs_dict_f["regular"][1] += 1
             else: 
                if random.random() >= 0.5 and jobs_dict_f["casual"][1]  < jobs_dict_f["casual"][0]:
                    v["Employment"] = "casual"
                    jobs_dict_f["casual"][1] += 1
                else: 
                    v["Employment"] = "unemployed"
                    jobs_dict_f["unemployed"][1] += 1
            elif v["Age"] in employed_ages[0]: 
                if random.random() < 0.4 and jobs_dict_f["student"][1]  < jobs_dict_f["student"][0]: 
                    v["Employment"] = "Student"
                    jobs_dict_f["student"][1] += 1
                else: 
                   v["Employment"] = "unemployed"
                   jobs_dict_f["unemployed"][1] += 1  
            elif v["Age"] == "10-14" :
                 v["Employment"] = "school"
                 
                 #in the evnet students in lower class need ot be paid
                 '''
                 if random.random() < 0.4 and v["Class"] == "Lower" and \
                 jobs_dict_f["child_labor_F"][1]  < jobs_dict_f["child_labor_F"][0]: 
                        v["Employment"] = "child_labor"
                        jobs_dict_f["child_labor_F"][1] += 1
                 else: 
                    v["Employment"] = "school"
                '''
        elif v["Employment"] == "TBD" and v["Gender"] == "M" and v["Age"] == "10-14":
             v["Employment"] = "school"
             
             
             #in the evnet students in lower class need ot be paid
             '''
             if random.random() < 0.5 and v["Class"] == "Lower" and \
                 jobs_dict_m["child_labor_M"][1]  < jobs_dict_m["child_labor_M"][0]: 
                        v["Employment"] = "child_labor"
                        jobs_dict_m["child_labor_M"][1] += 1
             else: 
               v["Employment"] = "school" 
             '''   
           
    return agents, jobs_dict_m, jobs_dict_f
        

def job_check(agents, jobs_dict_m, jobs_dict_f, employed_ages):
    
    for v in agents.values(): 
        if v["Employment"] == "TBD" and v["Gender"] == "F":
            for job, status in jobs_dict_f.items(): 
                if status[0] > status[1]:
                    v["Employment"] = job
                    break
        elif v["Employment"] == "TBD" and v["Gender"] == "M":        
            for job, status in jobs_dict_f.items(): 
                if status[0] > status[1]:
                    v["Employment"] = job
                    break
    return agents, jobs_dict_m, jobs_dict_f

def job_print(jobs_dict):
    
    
    
    for k, v in jobs_dict.items(): 
        if type(v) is list: 
            print (k, v[1])
        else: 
            print (k, v)

          

##################################################
#
# MAIN FUNCTION 
#
#################################################


def make_jobs(agents):
    
    #Assign jobs
    print ("\nPhase IV: There employment of Kianda is \n" )
    
    employed_ages = ["15-18", "18-25", "25-50", "51+"]
    
    agents, jobs_dict_m, jobs_dict_f = create_job_dict(agents, employed_ages)
    agents, jobs_dict_m, jobs_dict_f = assign_jobs(agents, jobs_dict_m, jobs_dict_f, employed_ages)
    agents, jobs_dict_m, jobs_dict_f = job_check(agents, jobs_dict_m, jobs_dict_f, employed_ages)
    
    print ("Male Employment: ")
    job_print(jobs_dict_m)
    print ("\nFemale Employment: ")
    job_print(jobs_dict_f)
    #print ("MALE EMPLOYMENT: ", jobs_dict_m, "\n")
    #print ("Female Employment: " , jobs_dict_f)
  
   

    return agents
    



