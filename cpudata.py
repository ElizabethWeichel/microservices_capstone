#import matplotlib.pyplot as plt
#import statistics
import os
#import json
#import subprocess as sub
#import numpy as np
import pandas as pd
#notes: sub.call calls the function in the terminal, but it does not get the output of the call read into the python file. os.popen actually reads in the output of the linux command into the python file.

currentallocation = os.popen('dzdo docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}"').readlines()
currallvals = []
for i in range(0, len(currentallocation)):
    currallvals.append(currentallocation[i].split())


df = pd.DataFrame(currallvals, columns = ['Name','CPU%'])
df1=df[df.Name.str[0]=='s']

df1.to_csv('cpuvals.csv',index=False)






