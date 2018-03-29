#!/bin/python
import os
import fnmatch
from parse_for_birl import *

subjects = {26,27,28,31,32,33,34,35,36,37,38,39,42,43,44,45,46,47,48,54,56,59,61,63,64} #60,62,65
tasks = 4

for subj in subjects:
    print "processing subject ", subj
    for file in os.listdir('./data/subj'+str(subj)):
        for i in range(1,tasks+1):
            if fnmatch.fnmatch(file, str(subj)+'_*_'+str(i)+'.data'):
                print "task ",i," file:", file
                trial_number = file.split("_")[1]
                parser = HumanDataParser('./data/subj'+str(subj)+"/"+file)
                parser.ProcessData()
                fh = open('baseline_birl/trajectories/'+str(subj)+'_'+str(trial_number)+'_'+str(i)+'.out','r')
                trajectories = []
                for line in fh:
                    line = line.strip()
                    if line.startswith("["):
                        trajectories.append(eval(line))
                parser.PlotTrajectory(trajectories,str(subj)+'_'+str(trial_number)+'_'+str(i))
