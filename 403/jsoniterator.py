#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 10:12:59 2022

@author: lizzieweichel
"""
import os
import json
import matplotlib.pyplot as plt
import numpy as np

#creating empty lists for each microservice to have data added
mongo_update_client = []
social_graph_mongo_update_client = []
social_graph_redis_update_client = []
follow_server = []
follow_with_username_server = []
user_mmc_get_user_id_client = []
get_user_id_server = []
follow_client = []
wrk2_api_user_follow = []

#the directory must be specified based upon where the .jsons are being outputted. 
#this directory corresponds to my personal computer, but can also be changed for the lab computer.
directory = '/Users/lizzieweichel/Desktop/jsons'
for filename in os.scandir(directory):
    if filename.name.endswith('.json'):
        with open(filename, 'r') as f:
            mylist = json.load(f)
            
            
            #there are 12 spans per json file.
            for i in range(0, 12):  
                opname = mylist['data'][0]['spans'][i]['operationName']
                
                #much like a switch statement, depending upon which microservice is being read at the time, the duration of that microservice is appended to its empty list
                if opname == 'social_graph_mongo_update_client':
                    social_graph_mongo_update_client.append(mylist['data'][0]['spans'][i]['duration'])
                
                elif opname == 'social_graph_redis_update_client':
                    social_graph_redis_update_client.append(mylist['data'][0]['spans'][i]['duration'])
                    
                elif  opname == 'follow_server':
                    follow_server.append(mylist['data'][0]['spans'][i]['duration'])
                    
                elif opname == 'follow_with_username_server':
                    follow_with_username_server.append(mylist['data'][0]['spans'][i]['duration'])
                    
                elif opname == 'user_mmc_get_user_id_client':
                    user_mmc_get_user_id_client.append(mylist['data'][0]['spans'][i]['duration'])
                    
                elif opname == 'get_user_id_server':
                    get_user_id_server.append(mylist['data'][0]['spans'][i]['duration'])
            
                
                elif opname == 'follow_client':
                    follow_client.append(mylist['data'][0]['spans'][i]['duration'])
                    
                elif opname == '/wrk2-api/user/follow':
                    wrk2_api_user_follow.append(mylist['data'][0]['spans'][i]['duration'])
     
#alldata is a multi-dimensional list of all of the microservice data arrays    
alldata = [social_graph_mongo_update_client, social_graph_redis_update_client, follow_server, follow_with_username_server, user_mmc_get_user_id_client,get_user_id_server,follow_client, wrk2_api_user_follow]
#names is a string list corresponding to the name of each microservice
names = ['social_graph_mongo_update_client', 'social_graph_redis_update_client', 'follow_server', 'follow_with_username_server', 'user_mmc_get_user_id_client','get_user_id_server','follow_client', 'wrk2_api_user_follow']

#pdf and cdf code cited from: https://www.geeksforgeeks.org/how-to-calculate-and-plot-a-cumulative-distribution-function-with-matplotlib-in-python/
#looping through each microservice's data and creating a cdf/pdf chart
for i in range(0, len(alldata)):
    count, bins_count = np.histogram(alldata[i], bins=10)
    pdf = count/sum(count)
    cdf = np.cumsum(pdf)

    plt.plot(bins_count[1:],pdf, color='red',label="PDF")
    plt.plot(bins_count[1:],cdf, color='blue',label="CDF")

    plt.legend()
    plt.title(names[i])
    plt.savefig(names[i])
    plt.figure()


            
