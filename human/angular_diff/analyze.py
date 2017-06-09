import sys
import scipy.stats
import numpy as np
import math
from os import listdir
from os.path import isfile,join
print("This program gives mean angular difference and std for each task (1-4), averaged across all subjects")

# get all .data files from subject data
if len(sys.argv) != 2:
    print("USAGE: python analyze.py [directory to the human result file]")

direct = sys.argv[1]
files = [f for f in listdir(direct)]
dataFiles = []
for f in files:
    dataFiles.append(direct + f)
dataFiles.sort()
num = len(dataFiles)

task1 = []
task2 = []
task3 = []
task4 = []
for f in dataFiles:
    fo = open(f, 'r')
#    print(f)
    for j,line in enumerate(fo):
        if j == 0: numTrials = int(line)
        else:
            if 1 <= j <= numTrials: task1 = np.append(task1, float(line))        
            elif numTrials < j <= numTrials * 2: task2 = np.append(task2, float(line))        
            elif numTrials * 2 < j <= numTrials * 3: task3 = np.append(task3, float(line))        
            elif numTrials * 3 < j <= numTrials * 4: task4 = np.append(task4, float(line))
    fo.close()
print(len(task1))
print("mean ang diff for task1: " + str(np.mean(task1)))      
print("std ang diff for task1: " + str(np.std(task1)))      
print("mean ang diff for task2: " + str(np.mean(task2)))      
print("std ang diff for task2: " + str(np.std(task2)))      
print("mean ang diff for task3: " + str(np.mean(task3)))      
print("std ang diff for task3: " + str(np.std(task3)))      
print("mean ang diff for task4: " + str(np.mean(task4)))      
print("std ang diff for task4: " + str(np.std(task4)))      
print("====================================================")
print("sem ang diff for task1: " + str(scipy.stats.sem(task1)))      
print("sem ang diff for task2: " + str(scipy.stats.sem(task2)))      
print("sem ang diff for task3: " + str(scipy.stats.sem(task3)))      
print("sem ang diff for task4: " + str(scipy.stats.sem(task4)))      
