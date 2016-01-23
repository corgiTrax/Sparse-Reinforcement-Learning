import scipy.io as sio  
import matplotlib.pyplot as plt  
import numpy as np 

# read and parse mat file
data = sio.loadmat("subj26parsed.mat")

subjNum = data["subjNum"][0,0]

# data for all 32 trials
pRes = data["pRes"]

maxTrial = 1
for trial in range(0, maxTrial):
    trialData = pRes[0][trial]
    
    trialNum = trialData["trialNum"][0,0][0,0]
    taskNum = trialData["taskNum"][0,0][0,0]
    print(taskNum)



# write data to a text file
