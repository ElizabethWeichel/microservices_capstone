import pandas as pd
from multiprocessing import Process
import threading
import time
import matplotlib.pyplot as plt
import statistics
import os
import json
import subprocess as sub
import numpy as np
import io

#beginning the code by allocating 10% of 1 CPU to socialnetwork_nginx-thrift_1 container.
os.popen('dzdo docker update --cpus=0.1 socialnetwork_nginx-thrift_1')

#creating a pandas dataframe for the CPU usage values to be appended to
cpuvalues=pd.read_csv('cpuvals.csv', usecols=['Name'])

#command is a list of two workload generation commands that the for loop will run through
command = ['/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 20 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10','/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 20 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10000']
mean=[]

#######################################################################################################
####################################beginning of for loop##############################################
#######################################################################################################
for i in range(0, 2):
    
    #performing workload generation command in terminal.
    #.readlines() will read the output of the workload generation command into the variable "latency"
    latency=os.popen(command[i]).readlines()
    #from trial, latency[4] is the array value that corresponds to the row of the terminal output with the end-to-end latency string in it
    x=latency[4].split()
    
    #index 0 of the row containing the e2e latency string is the index with the actual e2e value
    e2e=x[1]
    
    #there are different units used. We must get all of the units the same in order to compare
    if 'u' in e2e:
        e2e=e2e.split('u')
        mean.append(float(e2e[0]))
    elif 'm' in e2e:
        e2e=e2e.split('m')
        mean.append(float(e2e[0])*1000)
    elif 's' in e2e:
        e2e=e2e.split('s')
        mean.append(float(e2e[0])*1000000)
    
    #this line of code is reading in the CPU usage for the different containers. 
    #cpuvals.csv is created by cpudata.py (also in the repo)
    cpuvalues2=pd.read_csv('cpuvals.csv', usecols=['CPU%'])
    #we are adding a new column to the cpuvalues dataframe for each workload generation
    cpuvalues[i+1]=cpuvalues2

#here we assume that mean[0] is our target end to end latency
#if the higher workload is greater than the end to end of the lower workload, we allocate more cpu to the container
#it is unrealistic for these two workloads to have the same mean since one is much higher workload than the other, but I made these workloads this disparate for demo purposes.
if(mean[1]>=mean[0]):
    print("More CPU needs to be allocated. The mean end to end latency is higher with more requests per second.")
    #allocating more cpu to the socialnetwork_nginx-thrift_1 container
    os.popen('dzdo docker update --cpus=0.5 socialnetwork_nginx-thrift_1')
    
    #re-running the workload 2 command to see a change in the mean
    latency=os.popen(command[1]).readlines()
    x=latency[4].split()
    e2e=x[1]
    if 'u' in e2e:
        e2e=e2e.split('u')
        mean.append(float(e2e[0]))
    elif 'm' in e2e:
        e2e=e2e.split('m')
        mean.append(float(e2e[0])*1000)
    
    cpuvalues2=pd.read_csv('cpuvals.csv',usecols=['CPU%'])
    cpuvalues['Updated']=cpuvalues2
    

else:
    print("With higher workload request, the mean latency is less than or equal. Therefore, more CPU does not need to be allocated.")
    print(cpuvalues)

print(mean)
print(cpuvalues)


