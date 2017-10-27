import numpy as np
import sys

file = open(sys.argv[1]) #'angular_diffs.txt')

angles_data = {1:[],2:[],3:[],4:[]}

for line in file:
    line = line.strip()
    task = int(line.split(":")[0].split("_")[-1].split(".")[0])
    angles_data[task].append(float(line.split(":")[2]))

for task in angles_data:
    angles = angles_data[task]
    if len(angles) < 1:
        break
    print "task:",task, " err:", sum(angles)/len(angles),"+-", np.std(angles)/np.sqrt(len(angles))
