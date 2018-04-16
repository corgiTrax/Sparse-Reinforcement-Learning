#!/bin/python
import os
import fnmatch
from subprocess import Popen, PIPE

subjects = {26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 44, 45, 46, 47, 48, 54, 56, 59, 61, 63, 64} 
tasks = 4

eight_data = [ 26, 27, 28 ]

data = {}
for subj in subjects:
    data[subj] = {}
    for i in range(1,tasks+1):
        data[subj][i] = []
    print "subject :", subj
    for filename in os.listdir('../data/subj'+str(subj)):
        for i in range(1,tasks+1):
            if fnmatch.fnmatch(filename, str(subj)+'_*_'+str(i)+'.data'):
                trial_number = filename.split("_")[1]
                output_file = open('./output/'+str(subj)+"_"+str(trial_number)+"_"+str(i)+".out")
                print "task ", i," file:", filename
                weights = []
                weights_found = False
                for line in output_file:
                    line = line.strip()
                    line = line.rstrip(',')
                    if "Weights" in line:
                        weights_found = True
                        weights = [ float(x) if len(x) > 0 else 0 for x in line.split(":")[1].split(",") ]
                if weights_found:
                    weights.append(int(trial_number))
                    data[subj][i].append(weights)
                else:
                    print "Error ! No weights found for ", filename

    for i in range(1,tasks+1): # Tasks
        #print "Task", i
        for idx in range(len(data[subj][i])): # trials
            weights = data[subj][i][idx]
            total_weight = 0
            #print idx, weights
            for j in range(4):
                total_weight += abs(weights[j])
            if total_weight != 0.0:
                for j in range(4):
                    data[subj][i][idx][j] /= total_weight 
        #for weights in data[subj][i]:
        #    print weights

    for i in range(1,tasks+1):
            print "Eavluating Task", i
            # 1,2,3 -> 4
            # 1,2,4 -> 3
            # 1.3.4 -> 2
            # 2.3,4 -> 1
            for idx in range(len(data[subj][i])):
                weights = [0.0 , 0.0, 0.0, 0.0] # data[subj][i][idx]
                base_trial_number = data[subj][i][idx][-1] 
                print "trial under test: ",base_trial_number
                ct = 0
                for idx2 in range(len(data[subj][i])):
                    if idx2 != idx:
                       ct += 1
                       for w in range(4): # iterate through weights
                            weights[w] += data[subj][i][idx2][w]
                if ct == 0:
                    print "ERROR! Experiment data missing!"
                    continue
                for w in range(4): # iterate through weights
                    weights[w] /= ct

                #submit_file = open("test_"+str(subj)+"_"+str(base_trial_number)+"_"+str(i)+".submit", "w")
                #submit_file.write('+Group = "Grad"\n')
                #submit_file.write('+Project = "AI_ROBOTICS"\n')
                #submit_file.write('+ProjectDescription = "simulation of reward learning using bayesian inverse reinforcement learning algorithm"\n')

                output_file = './trajectories/'+str(subj)+"_"+str(base_trial_number)+"_"+str(i)+".out"
                log_file = './log/'+str(subj)+"_"+str(base_trial_number)+"_"+str(i)

                arguments = str(subj)+ " " + str(base_trial_number)+  " " +str(i)+ " " + str(weights[0])+ " " + str(weights[1])+ " " + str(weights[2])+ " " + str(weights[3])

                #submit_file.write('Executable = test_reward \n')
                #submit_file.write('arguments = '+ arguments +' \n')
                #submit_file.write('Output = '+ output_file + ' \n')
                #submit_file.write('Log = '+ log_file +'.log \n')
                #submit_file.write('Error = '+ log_file +'.err \n')
                #submit_file.write('\nQueue 1 \n ')

                output_file = open('./trajectories/'+str(subj)+"_"+str(base_trial_number)+"_"+str(i)+".out", "w")
                p = Popen(['./test_reward', str(subj), str(base_trial_number), str(i), str(weights[0]), str(weights[1]), str(weights[2]), str(weights[3])],stdout=PIPE, stderr=PIPE)
                out, err = p.communicate()
                output_file.write(out)
                output_file.close()
