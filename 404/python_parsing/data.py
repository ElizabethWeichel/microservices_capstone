#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 16:07:02 2023

@author: lizzieweichel
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
file='Stats.xlsx'
dfallocs=pd.read_excel(file,sheet_name='Allocations')
lamda=1
lamdas=str(lamda)
t=1999
ts=str(t)
x=np.linspace(0, t, t-1)
dfallocs=dfallocs.transpose()
dfallocs=dfallocs.drop('Unnamed: 0')

dfrews=pd.read_excel(file,sheet_name='Rewards')
dfrews=dfrews.transpose()
dfrews=dfrews.drop('Unnamed: 0')

alist=[[],[],[],[],[],[]]

rlist=[[],[],[],[],[],[]]

mysum=[0,0,0,0,0,0]
#Taking integral of reward
for i in range(0, 6):
    rlist[i]=dfrews[i].tolist()
    alist[i]=dfallocs[i].tolist()
#i=1
    mysum[i]=rlist[i][0]

avgs=[[],[],[],[],[],[]]
for i in range(0, len(rlist)):
    avgs[i].append(mysum[i]/1)
#for i in range(0, len(rlist)):
    for j in range(1, len(rlist[i])):
        mysum[i]+=rlist[i][j]
        avgs[i].append(mysum[i]/j)

#mysum=rlist[0]
#for i in range(1, len(rlist)):
#    mysum+=rlist[i]
#    averages.append(mysum/i)

#print('rlist: ',rlist)
plt.figure()
x2=np.linspace(0, t, t-1)
#plt.scatter(x2, avgs[0])
#plt.scatter(x2, avgs[1])
#plt.scatter(x2, avgs[2])
#plt.scatter(x2, avgs[3])
#plt.scatter(x2, avgs[4])
#plt.scatter(x2, avgs[5])

for i in range(0, len(alist)):
    plt.scatter(x, avgs[i],label=['ms',i])

plt.legend(loc='lower right')
plt.title('Average of the Past Rewards per Microservice')
plt.xlabel('Iteration')
plt.ylabel('Reward')
plt.savefig('Integral_reward'+lamdas)
#plt.scatter(x2, avgs[6])
#print(dfallocs[0])

#for i in range(0, 6):
#    
#    y=dfallocs[i]
#    plt.figure()
#    plt.scatter(x,y,s=10)
#dfallocs.plot.scatter(x, y=1)

plt.figure()
f, ax=plt.subplots(1)
#ax.scatter(x2, alist[0])
for i in range(0, len(alist)):
    plt.scatter(x,alist[i],label=['ms',i])
#plt.scatter(x2, alist[4])    
ax.set_ylim(ymin=0)
#ax.set_ymax(ymax=30)
plt.legend(loc='upper right')
plt.title("Allocation vs. Iteration")
plt.xlabel('Iteration')
plt.ylabel("Allocation")
plt.savefig('allocation'+lamdas)

#plt.yscale('log')

plt.figure()

for i in range(0, len(alist)):
    plt.scatter(x, dfrews[i])
#plt.scatter(x,dfrews[0])
plt.title("Reward vs. Iteration")
plt.xlabel("Iteration")
plt.ylabel("Reward")
plt.savefig('real_reward'+lamdas)

#print(dfallocs)