import time
import os
import pandas as pd
from multiprocessing import Process, Queue

#command contains the workload generation commands
command = ['/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 10 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10','/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 100 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 10000']
mean=[]

#cpu all function is the function that reads in the CPU usage values for each microservice
def cpuall(q):
    currentallocation = os.popen('dzdo docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}"').readlines()
    currallvals = []
    for i in range(0, len(currentallocation)):
        currallvals.append(currentallocation[i].split())


    df = pd.DataFrame(currallvals, columns = ['Name','CPU%'])
    df1=df[df.Name.str[0]=='s']
    #putting the value of the dataframe of CPU values into the queue
    q.put(df1)

#wrkld is the function that performs the workload generation
def wrkld(mycommand,q):
    latency=os.popen(mycommand).readlines()
    #putting the value of the end-to-end latency into the queue
    q.put(latency)

#######
#commented out the for loop temporarily to get it to work over one iteration. If one iteration can work, then can move on to for loop
#######
#for i in range(0, 2):
#    print(i)
#latency = sub.run(command[0],shell=True).readlines()
    #latency=os.popen(command[0]).readlines()
#l2=latency

#creating two processes that call the two above functions simultaneously
if __name__=='__main__':
    q=Queue()
         ####################
         #Attempting threading
         #t1=threading.Thread(target=cpuall)
         #t2=threading.Thread(target=wrkld,args=[command[i]])
         #t2.start()
         #time.sleep(2)
         #t1.start()
         ####################
    p1=Process(target=wrkld, args=(command[0],q,))
    p2=Process(target=cpuall,args=(q,))
    p1.start()
    time.sleep(10)
    p2.start()
    p1.join()
    p2.join()
    #print(latency)

#retrieving what has been put onto the queue during the two above functions. Currently having trouble retrieiving the dataframe from the queue
while not q.empty():                                                  
    data = q.get()                                                    
    time.sleep(1)                                                     
    print "get (loop: %s)" %loop                                      
    loop += 1
    
#######################
#Attempting to allocate and get the data from the queue are the lines below
######################
#x=[]
#for i in range(0, 5):
#    x.append(q.get())
#name, cpu = q.get()
#print(name)

#print(cpu)
#print(val1)
#print(val2)
#print(val3)
#print(val4)
#print(val5)
#print(x)
