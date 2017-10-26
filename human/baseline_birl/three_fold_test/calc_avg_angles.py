import numpy as np

file = open('angular_diffs.out')

angles_data = {1:[],2:[],3:[],4:[]}

for line in file:
    line = line.strip()
    task = int(line.split(":")[0].split("_")[-1].split(".")[0])
    angles_data[task].append(float(line.split(":")[2]))

for task in angles_data:
    angles = angles_data[task]
    print "task:",task, " err:", sum(angles)/len(angles),"+-", np.std(angles)/np.sqrt(len(angles))
