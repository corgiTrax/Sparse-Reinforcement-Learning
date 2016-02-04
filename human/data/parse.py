import scipy.io as sio  
import matplotlib.pyplot as plt  
import numpy as np 

# read and parse mat file
data = sio.loadmat("subj26parsed.mat")

subjNum = data["subjNum"][0,0] #subject's ID

# data for all 32 trials
pRes = data["pRes"]

maxTrial = 1 # 32 trials
for trial in range(0, maxTrial):
    trialData = pRes[0][trial]
    
    trialNum = trialData["trialNum"][0,0][0,0] # trial #
    taskNum = trialData["taskNum"][0,0][0,0] # task #, indicating which modules are running

    # get agent positions XZs
    agentXs = trialData["agentX"][0] # array
    agentZs = trialData["agentZ"][0] # array
    print(agentXs)

    # get object positions
    



# write data to a text file
