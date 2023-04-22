#import matplotlib.pyplot as plt
#import statistics
import os
#import json
#import subprocess as sub
#import numpy as np
import pandas as pd
#notes: sub.call calls the function in the terminal, but it does not get the output of the call read into the python file. os.popen actually reads in the output of the linux command into the python file.

#using a docker command to get the CPU usage for each container
#the output of the docker command is read into the variable currentallocation as a string
currentallocation = os.popen('dzdo docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}"').readlines()
currallvals = []

#since currentallocation is a string, it must be split to get usable data
for i in range(0, len(currentallocation)):
    currallvals.append(currentallocation[i].split())

#inputting the values in a dataframe
df = pd.DataFrame(currallvals, columns = ['Name','CPU%'])

#if there are multiple containers running, this line filters them by ones that begin with "s" to correspond to the socialnetwork application
df1=df[df.Name.str[0]=='s']

#outputting the dataframe values into a csv that is then read by e2elatency.py
df1.to_csv('cpuvals.csv',index=False)






