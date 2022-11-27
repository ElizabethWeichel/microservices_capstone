import os
import subprocess as sub
import json

command = ['/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 1 -c 1 -d 10 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 100','/home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/wrk -D exp -t 2 -c 2 -d 100 -L -s /home/ugrads/l/lweichel13/Work/repos/repos/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 1000']
#def linux_command1(cmdb):
#    sub.run(cmdb, shell=True)
#def linux_command2(cmda):
#    sub.run(cmda, shell=True)

#for i in range(0, 2):
    #print(i)
#sub.run(command[0],shell=True)
cmd="curl -s 'http://localhost:16686/api/traces?service=user-service&lookback=100s&prettyprint=true&limit=100'"
datum = os.popen(cmd).readlines()
#print(datum[0][0])
jsondata = json.loads(datum[0])
print(len(jsondata))
print(jsondata['data'][50]['spans'][8]['duration'])
#print(jsondata['data'][0]['spans'][0])
#print(jsonStr)
#myvals=json.loads(jsonStr)
#print(myvals[0][0])
#jsonFile=open('mydata2.json','w')
#jsonFile.write(myvals)
#jsonFile.close()
#print(jsonStr)
#for i in range(0, len(datum)):
#    print(datum['spans'])
#output = sub.Popen(cmd, stdout=sub.PIPE, shell=True)
#output=output.communicate()
#print(type(output))
#print(output[0][0])
#jsonObj = json.dumps(output)
#print(jsonObj)
#print(len(datum))
#print(datum[0][0:33])
#if __name__=='__main__':
        #threading.Thread(target=linux_command1, args=[command[0][0]]).start()
    #    t=threading.Thread(target=linux_command2, args=[command[i][1]])
    #    t.start()
    #sub.run(command[i][0],shell=True)
    #t.join()
