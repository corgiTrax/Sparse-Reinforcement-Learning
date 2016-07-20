from config import *
import world
import sys
from os import listdir
from os.path import isfile,join

# get all .data files from subject data
direct = sys.argv[1]
EVAL = sys.argv[2]
files = [f for f in listdir(direct)]
dataFiles = []
for f in files:
    if f.find(".data") != -1 and f.find(".dis") == -1 and f.find(".fit") == -1:
        dataFiles.append(direct + f)
#print(dataFiles)

errs = [[],[],[],[]]
for dataf in dataFiles:
    newTrial = world.Trial(dataf)
#    print("Current file: " + dataf)
    task = int(dataf[-6]) # 1,2,3,4
    if task != 5: #True:
        if EVAL == "o": # use own irl file
            irlFile = (dataf.replace("data", "result", 1)).split('.')[0]
#            print(irlFile,dataf)
            err = newTrial.visualize_result(irlFile)
        elif EVAL == "a": # use aggregated irl file
            irlFile = direct.replace("data", "result", 1) + "task" + str(task)
            err = newTrial.visualize_result(irlFile)
        errs[task-1].append(err)

mean_errs = []
for task, taskErr in enumerate(errs):
    mean_err = sum(taskErr)/float(len(taskErr))
#    print("Angular difference of task {} is: {}".format(task + 1, mean_err))
    print(mean_err)
    mean_errs.append(mean_err)

#print("Average error of all trials is: {}".format(sum(mean_errs)/float(len(mean_errs))))
