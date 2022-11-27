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

#currentallocation = os.popen('dzdo docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}"').readlines()
#currallvals = []

#for i in range(0, len(currentallocation)):
#    currallvals.append(currentallocation[i].split())


#df = pd.DataFrame(currallvals, columns = ['Name','CPU%'])

#currall2 = sub.call(['dzdo','docker','stats','socialnetwork_nginx-thrift_1','--no-stream'])
#print(currall2)
#print(df)
#colnames = ['Means 1','Means 2']
#cmddata=["curl -s 'http://localhost:16686/api/traces?service=user-service&lookback=10s&prettyprint=true&limit=100'","curl -s 'http://localhost:16686/api/traces?service=user-service&lookback=10s&prettyprint=true&limit=100'"]
command = ['/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 20 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10','/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 20 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10000']
mean=[]
def cpuall():
    currentallocation = os.popen('dzdo docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}"').readlines()
    currallvals = []
    for i in range(0, len(currentallocation)):
        currallvals.append(currentallocation[i].split())


    df = pd.DataFrame(currallvals, columns = ['Name','CPU%'])
    df1=df[df.Name.str[0]=='s']
    print(df1)

def wrkld(cmd):
    latency=os.popen(cmd).readlines()
    return latency

for i in range(0, 2):
#    print(i)
#latency = sub.run(command[0],shell=True).readlines()
    latency=os.popen(command[i]).readlines()
#l2=latency
    #if __name__=='__main__':
         #t1=threading.Thread(target=cpuall)
         #t2=threading.Thread(target=wrkld,args=[command[i]])
         #t2.start()
         #time.sleep(2)
         #t1.start()
    #     p1=Process(target=wrkld, args=(command[i]))
    #     p2=Process(target=cpuall)
    #     p1.start()
    #     time.sleep(2)
    #     p2.start()
    #     p1.join()
    #     p2.join()
    #t=threading.Thread(target=linux_command2, args=[command[i][1]])
    #    t.start()
    #sub.run(command[i][0],shell=True)
    #t1.join()
    #t2.join()
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

if(mean[1]>=mean[0]):
    print("More CPU needs to be allocated. The mean end to end latency is higher with more requests per second.")
else:
    print("With higher workload request, the mean latency is less than or equal. Therefore, more CPU does not need to be allocated.")
#df=pd.read_csv(pd.compat.StringIO(latency[4]))
#for i in range(0, len(latency)):
#df=pd.DataFrame(latency)
#print(df.loc[[4]])
#cols=df.head()
#print(cols)

#for col in df.columns:
#    print(col)
#latvals=df.loc[4]
#latvals.values.tolist()
#print(latvals[0])



