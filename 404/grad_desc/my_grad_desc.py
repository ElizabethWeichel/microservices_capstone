import hydra
import numpy as np
from microservice_architecture_simulator.registry import ENVS
import pandas as pd
import sys
import os
import psutil

import time
start=time.time()
#load1, load5, load15 = psutil.getloadavg()

print(psutil.cpu_percent(interval=1))

@hydra.main(config_path="conf", config_name="workload_example", version_base=None)
def main(conf):
    env_class = ENVS[conf["env"]]
    env = env_class(conf["env_config"])
    
    # episode_reward keeps track of the separate aggregate rewards when split_reward is used
    if conf["env_config"]["split_reward"]:
        episode_reward = np.zeros((1, len(list(conf["env_config"]["arch"]["initial_resource_alloc"].keys()))))
    else:
        episode_reward = 0
    
    obs = env.reset()
    
    eta=0.1
    
    trial=30
    a_k_m_1 = np.array([[trial,trial],
                    [trial,trial],
                    [trial,trial],
                    [trial,trial],
                    [trial,trial],
                    [trial,trial]],
                    dtype=np.float32,)
    obs1, rew_m_1, done, info,_ = env.step(a_k_m_1)
    
    first=29
    a_k=np.array([[first, first],
                    [first,first],
                    [first, first],
                    [first, first],
                    [first, first],
                    [first, first]],
                    dtype=np.float32,)
    obs1, rew_1, done, info,_ = env.step(a_k)
    #print(rew_1)
    
    dfallocs=pd.DataFrame()
    dflats=pd.DataFrame()
    dfrews=pd.DataFrame()
    
    
    itera=0
    
    nextaction=[0,0,0,0,0,0]

    steps=0
    while not done:
        eta=10/(steps+10)
       # print(itera)
       # print("ak_m1: ",a_k_m_1)
       # print("rew_m_1: ", rew_m_1)
       # print("a_k: ",a_k)
       # print('rew_1: ',rew_1)
       
        for i in range(0, len(rew_1)):
            grad_f=(abs(rew_1[i])-abs(rew_m_1[i]))/(a_k[i][0]-a_k_m_1[i][0])
            nextaction[i] = (a_k[i][0]-eta*grad_f)
            #grad_f=0
            #if(abs(rew_1[i])>abs(rew_m_1[i]))&(a_k[i][0]>a_k_m_1[i][0]): #decrease allocation. Reward worse w/ higher alloc
            #    grad_f=(abs(rew_1[i])-abs(rew_m_1[i]))/(a_k[i][0]-a_k_m_1[i][0])
            #    nextaction[i] = (a_k[i][0]-eta*grad_f)
            #    print("decreasing allocation")
            
            #elif((abs(rew_1[i])>abs(rew_m_1[i]))&(a_k[i][0]<a_k_m_1[i][0])): #increase alloc. Reward worse w/ lower alloc
            #    grad_f=(abs(rew_1[i])-abs(rew_m_1[i]))/(a_k[i][0]-a_k_m_1[i][0])
            #    nextaction[i] = (a_k[i][0]-eta*grad_f)
            #    print("increasing allocation")
            #elif((abs(rew_1[i])<abs(rew_m_1[i]))&(a_k[i][0]<a_k_m_1[i][0])): #decrease alloc. Reward better w/ lower alloc
            #    grad_f=(abs(rew_1[i])-abs(rew_m_1[i]))/(a_k[i][0]-a_k_m_1[i][0])
            #    nextaction[i] = (a_k[i][0]-eta*grad_f)
            #    print("decreasing alloc")
            
            #elif((abs(rew_1[i]<abs(rew_m_1[i])))&(a_k[i][0]>a_k_m_1[i][0])): #increase alloc. Reward better w/ higher alloc
            #    grad_f=(abs(rew_1[i])-abs(rew_m_1[i]))/(a_k[i][0]-a_k_m_1[i][0])
            #    nextaction[i] = (a_k[i][0]-eta*grad_f)
            #    print("increasing alloc")
       
        for i in range(0, len(nextaction)):
            if nextaction[i]<0:
                nextaction[i]=1
            
        
        for i in range(0, len(nextaction)):
            if abs(a_k[i][0]-nextaction[i])>5:
                #nextaction[i]=np.random.uniform(low=a_k[i][0]-.5,high=a_k[i][0]+.5)
               nextaction[i]=a_k[i][0]-.5
       
        #print(nextaction)
        a_k_p_1 = np.array(
            [
                [nextaction[0],nextaction[0]],
                [nextaction[1],nextaction[1]],
                [nextaction[2],nextaction[2]],
                [nextaction[3],nextaction[3]],
                [nextaction[4],nextaction[4]],
                [nextaction[5],nextaction[5]]],
            
                dtype=np.float32,
            )
        
        rew_m_1=rew_1
        a_k_m_1=a_k
        #lat_a_k_m_1=lat_a_k
        _, rew_1, done, info,_ = env.step(a_k_p_1)
        #print(f"obs: {a_k}, reward: {rew_1}\n")
        
        dfallocs[itera]=a_k_p_1[:,0]
        
        dfrews[itera]=rew_1
        
        a_k=a_k_p_1
        itera+=1
        mysum=[0,0,0,0,0,0]
        steps+=1
        
        #for i in range(0, len(rew_1)):
        #    rewards_all[i].append(rew_1[i])
        
        #    mysum[i]=rewards_all[i][0]
        
        #avgs=[[],[],[],[],[],[]]
        #for i in range(0, len(rewards_all)):
        #    avgs[i].append(mysum[i]/1)
        #for i in range(0, len(rewards_all)):
        #    for j in range(1, len(rewards_all[i])):
        #        mysum[i]+=rewards_all[i][j]
        #        avgs[i].append(mysum[i]/j)
                #print(avgs)
        #diff=[0,0,0,0,0,0]
        #for i in range(0, len(avgs)):
            #for j in range(1, len(avgs)):
        #    for j in range(1, len(avgs[i])):
        #        diff=avgs[i][j]-avgs[i][j-1]
        #        if abs(diff)<.01:
        #            consec[i]+=1
        #        else:
        #            consec[i]=0
        #for k in range(0, len(consec)):#\

        #    if consec[k]==10:
        #        within[k]=1
                        #print('MS ',k,'is scaled')
        #mysum4=0
        #for i in within:
        #    mysum4+=i
        #    if mysum4==len(within):
        #        done=True              
        
        #print(within)
        #print(itera)
        #print(f"obs: {obs}, reward: {reward}\n")
        episode_reward += np.array(rew_1)
    #df["Allocation"]=allocs
    #df["Latencies"]=lats
    #df["Reward"]=rews
    #df["Action"]=nexts
    #print(f" total episode reward: {episode_reward}")
    
    with pd.ExcelWriter('Stats.xlsx') as writer:
        
        dfallocs.to_excel(writer,sheet_name="Allocations")
        dflats.to_excel(writer,sheet_name='Latencies')
        dfrews.to_excel(writer,sheet_name="Rewards")

    #dfallocs=dfallocs.transpose()
    #dfallocs.plot(y=0)
    #plt.show
    #print(dfallocs)

if __name__ == "__main__":
    main()

end = time.time()
print("This program took ",end-start," seconds to execute.")

#cpu_usage=(load1/os.cpu_count())*100
#print("The CPU usage is: ",cpu_usage)

