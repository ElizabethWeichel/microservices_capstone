import os
import pandas as pd
import json
import time
import subprocess as sub
import json
import datetime
import numpy as np
######################################################################################################################
# Trial and error code to use the curl command to retrieve data from jaeger rather than the json outputter python code
######################################################################################################################
year=2023
month=2
day=13
df=pd.DataFrame()
command = ['dzdo /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 10 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10','dzdo /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 10 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10000']

cmd1="curl -s 'http://localhost:16686/api/traces?service=compose-post-service&'"
services=[]

start=datetime.datetime.now()
start=start+datetime.timedelta(0,5)
start=time.mktime(start.timetuple())
latency=os.popen(command[0]).readlines()
start=int(start)
start=str(start)
commandlook=cmd1+'start='+start+'&limit=1'
datum=os.popen(commandlook).readlines()
jsondata=json.loads(datum[0])
for j in range(0, len(jsondata['data'][0]['spans'])):
    services.append(jsondata['data'][0]['spans'][j]['operationName'])
print(jsondata['data'][0]['traceID'])
services_2=[]
for i in services:
    if i not in services_2:
        services_2.append(i)
services=services_2

df['Services']=services

for p in range(0, len(jsondata['data'][0]['spans'])):
    df.loc[df.Services==jsondata['data'][0]['spans'][p]['operationName'],"Rd 1"]=jsondata['data'][0]['spans'][p]['duration']

start=datetime.datetime.now()
start=start+datetime.timedelta(0,5)
start=time.mktime(start.timetuple())
#print(start)
latency=os.popen(command[0]).readlines()
start=int(start)
start=str(start)
commandlook=cmd1+'start='+start+'&limit=1'
datum=os.popen(commandlook).readlines()
jsondata=json.loads(datum[0])
#print(jsondata['data'])
for p in range(0, len(jsondata['data'][0]['spans'])):
    df.loc[df.Services==jsondata['data'][0]['spans'][p]['operationName'],"Rd 2"]=jsondata['data'][0]['spans'][p]['duration']
print(df)
print(jsondata['data'][0]['traceID'])
df.to_csv('jsondata.xlsx')
