# microservices_capstone
Description of files in repo: <br/>
  
**clearfiles.py**: clearing files in a directory using python. Not used in more developed scripts. <br/>
  
**cpudata.py**: gets the CPU% data for each container being used. Outputs to a .csv.<br/>
  
**cpuvals.csv**: output of cpudata.py<br/>
  
**e2elatency.py**: performs workload generation commands in a loop. Compares higher workload generation end-to-end latency with lower workload and specifies whether more cpu needs to be allocated.<br/>
  
**jaeger-realtime.py**: cited from online. This outputs what is going into the localhost of jaeger into .json files.<br/>
  
**multi.py**: multiprocessing used to attempt to get cpu data and generate workloads at same time.<br/>
  
**mydata.json**: reading from the terminal into a .json file to be parsed.<br/>
  
**newdata.py**: attempting to use a different command to get microservice level latencies.<br/>
  
**readfromterminal.py**: similar to e2elatency, but focused on microservice level latencies rather than end-to-end latency of different workloads. Not in use for project right now, but room to work on this in the future. Issue is that the service-level latencies are not changing after a new workload has been generated.<br/>
  
**whileloop.py**: psuedo-code for what a thresholding algorithm would look like. Does NOT actually update cpu allocation of a container, but has the command within (the command is commented out).<br/>
  
