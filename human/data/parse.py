import scipy.io as sio  
import matplotlib.pyplot as plt  
import numpy as np 
import copy as cp
np.set_printoptions(precision = 3, suppress = True, linewidth = 1000, threshold = 'nan')
ACC = 3 # rounding accuracy, 1mm

def parse(data_file):
    # read and parse mat file
    data = sio.loadmat(data_file)
    
    subjNum = data["subjNum"][0,0] #subject's ID
    
    # data for all 32 trials
    pRes = data["pRes"]
    
    maxTrial = 32 # 32 trials
    for trial in range(0, maxTrial):
        trialData = pRes[0][trial]
        
        trialNum = trialData["trialNum"][0,0][0,0] # trial #
        taskNum = trialData["taskNum"][0,0][0,0] # task #, indicating which modules are running
    
        # get agent positions XZs
        agentX = trialData["agentX"][0][0][0] # array
        agentZ = trialData["agentZ"][0][0][0] # array
        agentAngle = trialData["agentAngle"][0][0][0]

        # get object positions
        targetX = trialData["targ"][0][0]["posX"][0][0][0:-1, :] # 2D array, |time step| x |target number|
        targetZ = trialData["targ"][0][0]["posZ"][0][0][0:-1, :]# 2D array
        numStep, numTar = targetX.shape
        numStep2, numTar2 = targetZ.shape
        assert(numTar == numTar2),"target number not agreed!"
        assert(numStep == numStep2), "target number of steps not agreed!"
    
        obstX = trialData["obst"][0][0]["posX"][0][0][0:-1, :]# 2D array, |time step| x |target number| 
        obstZ = trialData["obst"][0][0]["posZ"][0][0][0:-1, :] # 2D array
        numStep2, numObst = obstX.shape
        numStep3, numObst2 = obstZ.shape
        assert(numObst == numObst2),"obst number not agreed!"
        assert(numStep == numStep2 and numStep2 == numStep3), "obst number of steps not agreed!"
    
        pathX = trialData["path"][0][0]["posX"][0][0][0:-1, :] # 2D array, |time step| x |target number| 
        pathZ = trialData["path"][0][0]["posZ"][0][0][0:-1, :] # 2D array
        numStep2, numPath = pathX.shape
        numStep3, numPath2 = pathZ.shape
        assert(numPath == numPath2),"path number not agreed!"
        assert(numStep == numStep2 and numStep2 == numStep3), "path number of steps not agreed!"
        # get rid of the -100s at the end of path positions
        for i in range(numPath):
            if pathX[0][i] == -100: indexToRm = i; break
        pathX = pathX[:, 0:indexToRm]
        pathZ = pathZ[:, 0:indexToRm]    
        numStep2, numPath = pathX.shape
        numStep3, numPath2 = pathZ.shape
        assert(numPath == numPath2),"path number not agreed after truncation!"
    
        # get elevator position too
        # note that elevator positions are reversed each time
        # for subj#26, the first elevator is at the beginning of the path
        if trial % 2 == 1:
            elevX = cp.deepcopy(pathX[:, -1])
            elevZ = cp.deepcopy(pathZ[:, -1])
        else:
            elevX = cp.deepcopy(pathX[:, 0])
            elevZ = cp.deepcopy(pathZ[:, 0])

        # write data to a text file
        filename = "subj" + str(subjNum) + '/' + str(subjNum) + "_" + str(trialNum) + "_" + str(taskNum) + ".data"
        output_file = open(filename, 'w')
        # build time series data
        for t in range(numStep):
            output_file.write(str(t) + '#')
            # agent
            output_file.write(str(round(agentX[t],ACC)) + ',' + str(round(agentZ[t],ACC)) + ',' + str(round(agentAngle[t],ACC)) + '#')
            # targets
            for i in range(numTar):
                if not(targetX[t][i] == -100):
                    output_file.write(str(round(targetX[t][i],ACC)) + ',' + str(round(targetZ[t][i], ACC)) + ';') 
            output_file.write('#')
            # obstacles
            for i in range(numObst):
                if not(obstX[t][i] == -100):
                    output_file.write(str(round(obstX[t][i],ACC)) + ',' + str(round(obstZ[t][i], ACC)) + ';') 
            output_file.write('#')
            # paths
            for i in range(numPath):
                output_file.write(str(round(pathX[t][i],ACC)) + ',' + str(round(pathZ[t][i], ACC)) + ';') 
            output_file.write('#')
            # elevator
            output_file.write(str(round(elevX[t],ACC)) + ',' + str(round(elevZ[t],ACC)))
            output_file.write('\n') 
        output_file.close()

parse("subj26parsed.mat")
