#!/bin/python
import os
import fnmatch
from subprocess import Popen, PIPE

subjects = {26,27,28,31,32,33,34,35,36,37,38,39,61,63,64} #60,62,65
tasks = 4

for subj in subjects:
    print "processing subject ", subj
    for file in os.listdir('../data/subj'+str(subj)):
        for i in range(1,tasks+1):
            if fnmatch.fnmatch(file, str(subj)+'_*_'+str(i)+'.data'):
                print "task ",i," file:", file
                trial_number = file.split("_")[1]
                print "executing: ./feature_birl_test",str(subj),trial_number,str(i)
                output_file = open('./output/'+str(subj)+"_"+trial_number+"_"+str(i)+".out", "w")
                p = Popen(['./feature_birl_test',str(subj),str(trial_number),str(i)], stdout=PIPE, stderr=PIPE)
                out, err = p.communicate()
                output_file.write(out)
