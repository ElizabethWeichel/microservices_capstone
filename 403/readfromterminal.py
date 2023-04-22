import pandas as pd
import threading
import matplotlib.pyplot as plt
import statistics
import os
import json
import subprocess as sub
import numpy as np

means=[]

#initializing dataframe with the names of each microservice.
names = ['social_graph_mongo_update_client', 'social_graph_redis_update_client', 'follow_server', 'follow_with_username_server', 'user_mmc_get_user_id_client','get_user_id_server','follow_client', 'wrk2_api_user_follow']
df = pd.DataFrame()
df['Names']=names
print(df)
##################################################################################################################
#this section is included as an attempt to perform microprocessing and get CPU usage at the same time as workload generation
#currentallocation = os.popen('dzdo docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}"').readlines()
#currallvals = []

#for i in range(0, len(currentallocation)):
#    currallvals.append(currentallocation[i].split())


#df = pd.DataFrame(currallvals, columns = ['Name','CPU%'])

#currall2 = sub.call(['dzdo','docker','stats','socialnetwork_nginx-thrift_1','--no-stream'])
#print(currall2)
#print(df)
##################################################################################################################

colnames = ['Means 1','Means 2']

#cmddata has the commands that look back and retrieve json traces from jaeger.
cmddata=["curl -s 'http://localhost:16686/api/traces?service=user-service&lookback=10s&prettyprint=true&limit=100'","curl -s 'http://localhost:16686/api/traces?service=user-service&lookback=10s&prettyprint=true&limit=100'"]

#command contains two different workload generation codes.
command = ['/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 100 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 100','/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 2 -c 2 -d 100 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10000']

##################################################################################################################
#beginning of for loop
#pseudo code:
    #loops through the length of "command" array
    #for each loop it generates a workload, it then reads back json files from jaeger that have the microservice-level latencies
    #parses the jsons read in from jaeger
    #prints the average latency of each microservice to an array
    
for i in range(0, 2):
    #running the workload generation command
    sub.run(command[i],shell=True)
    
    #attempt to use threading to get workload and cpu usage data simulatenously
    #if __name__=='__main__':
        #threading.Thread(target=linux_command1, args=[command[0][0]]).start()
    #    t=threading.Thread(target=linux_command2, args=[command[i][1]])
    #    t.start()
    #sub.run(command[i][0],shell=True)
    #t.join()
    
    #reading in .json data from jaeger
    mydata=os.popen(cmddata[i]).readlines()
    jsondata=json.loads(mydata[0])

    mongo_update_client = []
    social_graph_mongo_update_client = []
    social_graph_redis_update_client = []
    follow_server = []
    follow_with_username_server = []
    user_mmc_get_user_id_client = []
    get_user_id_server = []
    follow_client = []
    wrk2_api_user_follow = []
    
    #parsing the json data from jaeger
    for p in range(0, len(jsondata['data'])):
        if len(jsondata['data'][p]['spans'])==12:

            for q in range(0, 12):


                #mongo_update_client = []
                #social_graph_mongo_update_client = []
                #social_graph_redis_update_client = []
                #follow_server = []
                #follow_with_username_server = []
                #user_mmc_get_user_id_client = []
                #get_user_id_server = []
                #follow_client = []
                #wrk2_api_user_follow = []
    
    #this section pertained to a different method for reading in .jsons. When I changed to the terminal command rather than a python file, I did not need this method.
    #directory = '/home/ugrads/l/lweichel13/Work/repos/pythontrial/user-service'
    #for filename in os.scandir(directory):
     #   if filename.name.endswith('.json'):
      #      with open(filename, 'r') as f:
       #         mylist = json.load(f)

            #for i in range(0, 10):
                #names[i]=mylist['data'][0]['spans'][i]['operationName']
        #        if len(mylist['spans'])==12:
#
 #                   for i in range(0, 12):
#                opname = mylist['spans'][i]['operationName']
                
                #assigning the duration of each microservice to that microservice's array
                opname = jsondata['data'][p]['spans'][q]['operationName']
                #print(opname)
                if opname == 'social_graph_mongo_update_client':
                    social_graph_mongo_update_client.append(jsondata['data'][p]['spans'][q]['duration'])
                
                elif opname == 'social_graph_redis_update_client':
                    social_graph_redis_update_client.append(jsondata['data'][p]['spans'][q]['duration'])

                elif  opname == 'follow_server':
                    follow_server.append(jsondata['data'][p]['spans'][q]['duration'])

                elif opname == 'follow_with_username_server':
                    follow_with_username_server.append(jsondata['data'][p]['spans'][q]['duration'])

                elif opname == 'user_mmc_get_user_id_client':
                    user_mmc_get_user_id_client.append(jsondata['data'][p]['spans'][q]['duration'])

                elif opname == 'get_user_id_server':
                    get_user_id_server.append(jsondata['data'][p]['spans'][q]['duration'])


                elif opname == 'follow_client':
                    follow_client.append(jsondata['data'][p]['spans'][q]['duration'])

                elif opname == '/wrk2-api/user/follow':
                     wrk2_api_user_follow.append(jsondata['data'][p]['spans'][q]['duration'])
    
    #have a larger array with all of the microservice latencies for all microservices
    alldata = [social_graph_mongo_update_client, social_graph_redis_update_client, follow_server, follow_with_username_server, user_mmc_get_user_id_client,get_user_id_server,follow_client, wrk2_api_user_follow]
    means=[]
    
    #creating a dataframe with the means of each of the microservices. It will append to the dataframe as the for loop generates more workloads.
    for i in range(0, len(alldata)):
        #print(alldata[i])
        means.append(statistics.mean(alldata[i]))
    #df[i+1]=means
    print(means)
    #print() 

###############################################################################
#pdf and cdf creation, not needed every time for testing.
#pdf and cdf code cited from: https://www.geeksforgeeks.org/how-to-calculate-and-plot-a-cumulative-distribution-function-with-matplotlib-in-python/
#for i in range(0, len(alldata)):
#    count, bins_count = np.histogram(alldata[i], bins=10)
#    pdf = count/sum(count)
#    cdf = np.cumsum(pdf)
#
#    plt.plot(bins_count[1:],pdf, color='red',label="PDF")
#    plt.plot(bins_count[1:],cdf, color='blue',label="CDF")
#
#    plt.legend()
#    plt.title(names[i])
#    plt.savefig(names[i])
#    plt.figure()

###############################################################################
#######Comparing data to SLO to make a resource allocation decision############
###############################################################################
#Need to set SLO's to have something to compare the mean to...
    #means=[]
    #for j in range(0, len(alldata)):
    #    #print(names[i],statistics.mean(alldata[i]))
    #    means.append(statistics.mean(alldata[i]))
    #print(means)    

print(means)

