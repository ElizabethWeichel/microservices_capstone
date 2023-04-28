import hydra
import numpy as np
from microservice_architecture_simulator.registry import ENVS
import pandas as pd



@hydra.main(config_path="conf", config_name="workload_example", version_base=None)
def main(conf):
    myiter=0
    # For now just initialize env and test its working TODO add replace with script
    env_class = ENVS[conf["env"]]
    env = env_class(conf["env_config"])
    done = False
    episode_reward = 0
    obs = env.reset()
    action = np.array(
            [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
            dtype=np.float32,
        )  # Increase all resource caps by 1 unit
    enum=0
    obs, init_reward, done, info = env.step(action)
    high = 1
    low = -1
    print(f"obs: {obs}, reward: {init_reward}\n")
    print(len(obs))
    my_r0 = init_reward
    df=pd.DataFrame()
    nodes=conf["env_config"]["jobs"]["path"]["Job1"]
    nodes_copy=nodes
    node_rewards=[0]*len(nodes)
    
    df['nodes']=nodes
    df['reward']=node_rewards
    
    for i in range(0, len(nodes)):
        enum=0
        action[i][0]=high
        action[i][1]=high
        
        obs, reward, done, info = env.step(action)
        #print(f"obs: {obs}, reward: {reward}\n")
        node_rewards[i]=reward
        action[i][0]=low
        action[i][1]=low
        if i > 0:
            action[i-1]=[0,0]
    
    print(node_rewards)
    
    nextnode=np.copy(node_rewards)
    action = np.array(
            [[0, 0], [0, 0], [0, 0], [-1, -1], [0, 0], [0, 0]],
            dtype=np.float32,
        )  
    obs, init_reward, done, info = env.step(action)
    #print(f"obs: {obs}, reward: {reward}\n")
    better = False
    action = np.array(
            [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
            dtype=np.float32,
        )
    my_iter_for_end = 0
    everything=np.random.rand(len(nodes))
    mylist=[0,0,0,0]
    while done == False:
        myiter+=1
        
        for i in range(0, len(nodes)):
            if (mylist[i]=='maxed' or mylist[i]=='maxed and corrected'):
                everything[i]=1
        
        tested=np.all(everything==1)
        if tested==True:
            print('not beneficial to increase any')
            print(myiter)
            break
        enum = 1

        if my_iter_for_end == len(nodes):
            break
        
        #highest=np.argmax(node_rewards)
        #print(highest)
        for i in range(0, len(nodes)):
            if mylist[i]=='maxed and corrected':
                action[i]=[0,0]

            if mylist[i]=='maxed':
                action[i]=[-1,-1]
                mylist[i]='maxed and corrected'
        
         #gets the allocation back down
        
        highest=int(np.argmax(nextnode))
        #if nodes[highest]!='maxed':
        #    continue
        #else:
        #    mymin=np.argmin(node_rewards)
        #    for i in range(0, len(node_rewards)):
        #        if node_rewards(i)>mymin & node_rewards[i]<node_rewards[highest]:
        #            mymax=node_rewards[i]
        #    highest=node_rewards.index(mymax)
       
        prev_reward=node_rewards[highest]

        
        action[highest]=[1,1] # Increase all resource caps by 1 unit
        obs, reward, done, info = env.step(action)
        print(f"obs: {obs}, reward: {reward}\n")
        episode_reward += reward
        if reward < prev_reward:
            better = True
            print('it is not beneficial to continue increasing node',nodes[highest])
            my_iter_for_end+=1
            mylist[highest]='maxed'
            nextnode[highest]-=1000
            #action[highest]=[-5,-5]
            
        else:
            better = False
            node_rewards[highest]=reward
           #action[highest]=[-5,-5]
        print(node_rewards)
        print(nodes)
        print(nextnode)
        print(mylist)
    print(f" total episode reward: {episode_reward}")


if __name__ == "__main__":
    main()
