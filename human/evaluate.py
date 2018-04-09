from config import *
import world
import sys
from os import listdir
from os.path import isfile,join
from scipy.stats import sem
import numpy

# get all .data files from subject data
if len(sys.argv) < 2:
    print("USAGE: python evaluate.py [directory to the human data file]")

direct = sys.argv[1]
files = [f for f in listdir(direct)]
dataFiles = []
for f in files:
    if f.find(".data") != -1 and f.find(".dis") == -1 and f.find(".fit") == -1 and f.find(".png") == -1:
        dataFiles.append(direct + f)

errs = [[],[],[],[]]
errsFw = [[],[],[],[]]
for dataf in dataFiles:
    newTrial = world.Trial(dataf)
#    print("Current data file: " + dataf)
    task = int(dataf[-6]) # 1,2,3,4
    irlFile = (dataf.replace("data", "result", 1)).split('.')[0]
#    print("Using irl result file: " + irlFile)
    err, errFw = newTrial.visualize_result(irlFile)
    errs[task-1].append(err)
    errsFw[task-1].append(errFw)

print(len(errs[0]))
for taskErr in errs:
    for err in taskErr:
        print(err)

mean_errs = [] # across 4 tasks
for task, taskErr in enumerate(errs):
    mean_err = numpy.mean(taskErr) 
    std_err = sem(taskErr)
    print("Angular difference of task {} is: {}, std is {}".format(task + 1, mean_err, std_err))
    mean_errs.append(mean_err)

print("Average error of all trials is: {}".format(sum(mean_errs)/float(len(mean_errs))))
