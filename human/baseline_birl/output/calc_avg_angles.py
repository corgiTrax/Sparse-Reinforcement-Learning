import numpy as np

file = open('diffs.txt')

angles_data = {1:[],2:[],3:[],4:[]}

ct = 0
for line in file:
    ct += 1
    print "processing line", ct
    line = line.strip()
    task = int(line.split(":")[0].split("_")[-1].split(".")[0])
    angles_data[task].append(float(line.split(":")[2].split("'")[0]))

for task in angles_data:
    angles = angles_data[task]
    print "task:",task, " err:", sum(angles)/len(angles),"+-", np.std(angles)/np.sqrt(len(angles))
