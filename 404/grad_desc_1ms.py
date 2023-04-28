import hydra
import numpy as np
from microservice_architecture_simulator.registry import ENVS
import pandas as pd



@hydra.main(config_path="conf", config_name="workload_example", version_base=None)
def main(conf):
    env_class = ENVS[conf["env"]]
    env = env_class(conf["env_config"])
    done = False
    df=pd.DataFrame(columns=['Allocation','Latencies','Reward'])
    print(df)
    # episode_reward keeps track of the separate aggregate rewards when split_reward is used
    if conf["env_config"]["split_reward"]:
        episode_reward = np.zeros((1, len(list(conf["env_config"]["arch"]["initial_resource_alloc"].keys()))))
    else:
        episode_reward = 0
    obs = env.reset()
    a_k = np.array([[0.1,0.1],
                    [0.0,0.0],
                    [0.0,0.0],
                    [0.0,0.0],
                    [0.0,0.0],
                    [0.0,0.0]],
                    dtype=np.float32,)
    obs1, lat_a_k, rew_1, done, info = env.step(a_k)
    print(rew_1)
    eta=0.00001
    print(a_k[0][0])
    a_k_m_1=[0.0]
    lat_a_k_m_1=[0.0]
    rew_m_1=0.0
    dec = 'False'
    allocs=[]
    lats=[]
    rews=[]
    nexts=[]
    while not done:
        allocs.append(a_k[0][0])
        lats.append(lat_a_k[0])
        rews.append(rew_1)
        
        print("Rew_1: ",rew_1)
        print("Rew_m_1: ",rew_m_1)
        print("a_k: ",a_k[0][0])
        print("a_k_m_1: ",a_k_m_1[0])
        if(abs(rew_1)>abs(rew_m_1))&(a_k[0][0]>a_k_m_1[0]): #decrease allocation. Reward worse w/ higher alloc
            grad_f=(abs(rew_1)-abs(rew_m_1))/(a_k[0][0]-a_k_m_1[0])
            nextaction = (a_k[0][0]-eta*grad_f)/2
            print("decreasing allocation")
            if(nextaction>0):
                nextaction = -nextaction
        elif((abs(rew_1)>abs(rew_m_1))&(a_k[0][0]<a_k_m_1[0])): #increase alloc. Reward worse w/ lower alloc
            grad_f=(abs(rew_1)-abs(rew_m_1))/(a_k[0][0]-a_k_m_1[0])
            nextaction = (a_k[0][0]-eta*grad_f)/2
            print("increasing allocation")
        elif((abs(rew_1)<abs(rew_m_1))&(a_k[0][0]<a_k_m_1[0])): #decrease alloc. Reward better w/ lower alloc
            grad_f=(abs(rew_1)-abs(rew_m_1))/(a_k_m_1[0]-a_k[0][0])
            nextaction = (a_k[0][0]-eta*grad_f)/2
            print("decreasing alloc")
            if(nextaction>0):
                nextaction = -nextaction
        else:
            grad_f=(abs(rew_1)-abs(rew_m_1))/(a_k_m_1[0]-a_k[0][0])
            nextaction = (a_k[0][0]-eta*grad_f)/2
            print("increasing alloc")
        nexts.append(nextaction)
        #print(nextaction)
        print(grad_f)
        print(nextaction)
        nextaction = np.array(
            [
                [nextaction, nextaction],
                [0.0,0.0],
                [0.0,0.0],
                [0.0,0.0],
                [0.0,0.0],
                [0.0,0.0]],
            
            dtype=np.float32,
            )
            
          # Increase all resource caps by 0.5 unit
        rew_m_1=rew_1
        a_k_m_1[0]=a_k[0][0]
        lat_a_k_m_1[0]=lat_a_k[0]
        a_k, lat_a_k, rew_1, done, info = env.step(nextaction)
        print(f"obs: {a_k}, latency: {lat_a_k}, reward: {rew_1}\n")
        
        #print(f"obs: {obs}, reward: {reward}\n")
        episode_reward += np.array(rew_1)
    df["Allocation"]=allocs
    df["Latencies"]=lats
    df["Reward"]=rews
    df["Action"]=nexts
    print(f" total episode reward: {episode_reward}")
    df.to_excel('Stats.xlsx')
if __name__ == "__main__":
    main()
