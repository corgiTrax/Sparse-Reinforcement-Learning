#!/bin/python
import os
import fnmatch
from subprocess import Popen, PIPE

subjects = {26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 44, 45, 46, 47, 48, 54, 56, 59, 61, 63, 64} #60,62,65
tasks = 4

for subj in subjects:
    print "processing subject ", subj
    for file in os.listdir('../data/subj'+str(subj)):
        for i in range(1,tasks+1):
            if fnmatch.fnmatch(file, str(subj)+'_*_'+str(i)+'.data'):
                print "task ",i," file:", file
                trial_number = file.split("_")[1]
                print "generating submit file for: ./reward_learning",str(subj),trial_number,str(i)

                submit_file = open(str(subj)+"_"+trial_number+"_"+str(i)+".submit", "w")
                submit_file.write('+Group = "Grad"\n')
                submit_file.write('+Project = "AI_ROBOTICS"\n')
                submit_file.write('+ProjectDescription = "simulation of reward learning using bayesian inverse reinforcement learning algorithm"\n')

                output_file = './output/'+str(subj)+"_"+trial_number+"_"+str(i)+".out"
                log_file = './log/'+str(subj)+"_"+trial_number+"_"+str(i)

                arguments = str(subj)+" "+str(trial_number)+" "+str(i)

                submit_file.write('Executable = reward_learning \n')
                submit_file.write('arguments = '+ arguments +' \n')
                submit_file.write('Output = '+ output_file + ' \n')
                submit_file.write('Log = '+ log_file +'.log \n')
                submit_file.write('Error = '+ log_file +'.err \n')
                submit_file.write('\nQueue 1 \n ')
