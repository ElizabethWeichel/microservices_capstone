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

mongo_update_client = []
social_graph_mongo_update_client = []
social_graph_redis_update_client = []
follow_server = []
follow_with_username_server = []
user_mmc_get_user_id_client = []
get_user_id_server = []
follow_client = []
wrk2_api_user_follow = []

directory = '/Users/lizzieweichel/Desktop/jsons'
for filename in os.scandir(directory):
    if filename.name.endswith('.json'):
        with open(filename, 'r') as f:
            mylist = json.load(f)
            
            #for i in range(0, 10):
                #names[i]=mylist['data'][0]['spans'][i]['operationName']
            
            for i in range(0, 12):  
                opname = mylist['data'][0]['spans'][i]['operationName']
                
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
      
alldata = [social_graph_mongo_update_client, social_graph_redis_update_client, follow_server, follow_with_username_server, user_mmc_get_user_id_client,get_user_id_server,follow_client, wrk2_api_user_follow]
names = ['social_graph_mongo_update_client', 'social_graph_redis_update_client', 'follow_server', 'follow_with_username_server', 'user_mmc_get_user_id_client','get_user_id_server','follow_client', 'wrk2_api_user_follow']

#pdf and cdf code cited from: https://www.geeksforgeeks.org/how-to-calculate-and-plot-a-cumulative-distribution-function-with-matplotlib-in-python/
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


            
