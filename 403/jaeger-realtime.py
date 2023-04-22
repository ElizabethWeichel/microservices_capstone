#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:02:11 2022

@author: lizzieweichel
"""
#!/usr/bin/env python
#cited from: https://github.com/Ashmita152/jaeger-datasets/blob/master/bookinfo/extract.py
import pandas as pd
import os
import json
import requests

JAEGER_TRACES_ENDPOINT = "http://localhost:16686/api/traces?limit=20000&"
JAEGER_TRACES_PARAMS = "service="

def get_traces(service):
    """
    Returns list of all traces for a service
    """
    url = JAEGER_TRACES_ENDPOINT + JAEGER_TRACES_PARAMS + service
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise err

    response = json.loads(response.text)
    traces = response["data"]
    return traces

JAEGER_SERVICES_ENDPOINT = "http://localhost:16686/api/services"

def get_services():
    """
    Returns list of all services
    """
    try:
        response = requests.get(JAEGER_SERVICES_ENDPOINT)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise err
        
    response = json.loads(response.text)
    services = response["data"]
    return services

def write_traces(directory, traces):
    """
    Write traces locally to files
    """
    for trace in traces:
        traceid = trace["traceID"]
        path = directory + "/" + traceid + ".json"
        with open(path, 'w') as fd:
            fd.write(json.dumps(trace))

# Pull traces for all the services & store locally as json files
for service in get_services():
    if not os.path.exists(service):
        os.makedirs(service)
    traces = get_traces(service)
    write_traces(service, traces)

    #currentallocation = os.popen('dzdo docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}"').readlines()
    #currallvals = []

   # for i in range(0, len(currentallocation)):
  #      currallvals.append(currentallocation[i].split())


 #   df = pd.DataFrame(currallvals, columns = ['Name','CPU%'])

#print(df)







