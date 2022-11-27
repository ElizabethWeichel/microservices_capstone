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
means=[]
names = ['social_graph_mongo_update_client', 'social_graph_redis_update_client', 'follow_server', 'follow_with_username_server', 'user_mmc_get_user_id_client','get_user_id_server','follow_client', 'wrk2_api_user_follow']
df = pd.DataFrame()
df['Names']=names
print(df)

command = ['/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 20 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10','/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 20 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10000']
mean=[0,0]
while(mean[1]>=mean[0]):
    for i in range(0, 2):
        latency=os.popen(command[i]).readlines()
        print(latency[4])
        x=latency[4].split()
        print(x)
        e2e=x[1]
    #e2e=e2e.split('u')
    #e2e=e2e.split('m')
        if 'u' in e2e:
            e2e=e2e.split('u')
            mean.append(float(e2e[0]))
        elif 'm' in e2e:
            e2e=e2e.split('m')
            mean.append(float(e2e[0])*1000)
    #mean.append(e2e[0])
        cpuvalues=pd.read_csv('cpuvals.csv')
        print(cpuvalues)
#print(e2e[0])
#print(opname)
    print(mean)
    currlargeall = cpuvalues.iloc[0]['CPU%']
    currlargeall=currlargeall.split('%')
    currlargeall=float(currlargeall[0])
    if(mean[1]>=mean[0]):
        print("More CPU needs to be allocated. The mean end to end latency is higher with more requests per second.")
        #increase CPU allocation here of nginx container.
        #the reason that 80% is chosen here is because of prior data collection that shows nginx container using upwards of 74% of CPU.
        #os.popen("dzdo docker run socialnetwork_nginx-thrift_1 --cpus=".8" ubuntu /bin/bash")
    else:
        print("With higher workload request, the mean latency is less than or equal. Therefore, more CPU does not need to be allocated.")
    

