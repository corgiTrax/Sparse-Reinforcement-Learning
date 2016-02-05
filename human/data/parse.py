import scipy.io as sio  
import matplotlib.pyplot as plt  
import numpy as np 

np.set_printoptions(precision = 4, suppress = True, linewidth = 1000, threshold = 'nan')

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
    agentXs = trialData["agentX"][0][0][0] # array
    agentZs = trialData["agentZ"][0][0][0] # array

    # get object positions
    targetX = trialData["targ"][0][0]["posX"][0][0] # 2D array, |time step| x |target number| 
    targetZ = trialData["targ"][0][0]["posZ"][0][0] # 2D array

    obstX = trialData["obst"][0][0]["posX"][0][0] # 2D array, |time step| x |target number| 
    obstZ = trialData["obst"][0][0]["posZ"][0][0] # 2D array

    pathX = trialData["path"][0][0]["posX"][0][0] # 2D array, |time step| x |target number| 
    pathZ = trialData["path"][0][0]["posZ"][0][0] # 2D array

    # get elevator position too

    # build time series data


    # write data to a text file
