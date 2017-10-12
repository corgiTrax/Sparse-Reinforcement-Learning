#!/bin/python
import os
import fnmatch
from subprocess import Popen, PIPE

subjects = {26,27,28,31,32,33,34,35,36,37,38,39,61,63,64} #60,62,65
tasks = 4

data = {}
for subj in subjects:
    data[subj] = {}
    for i in range(1,tasks+1):
        data[subj][i] = []
    print "subject :", subj
    for file in os.listdir('../../data/subj'+str(subj)):
        for i in range(1,tasks+1):
            if fnmatch.fnmatch(file, str(subj)+'_*_'+str(i)+'.data'):
                print "task ",i," file:", file
                trial_number = file.split("_")[1]
                output_file = open('./'+str(subj)+"_"+trial_number+"_"+str(i)+".out")
                for line in output_file:
                    line = line.strip()
                    if line.startswith("Feature"):
                        weights = [float(x) if len(x) > 0 else 0 for x in line.split(":")[1].split(",")]
                data[subj][i].append(weights)

    for i in range(1,tasks+1):
        print "Task", i, ":" ,data[subj][i]
