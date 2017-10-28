import numpy as np
import sys

file = open(sys.argv[1]) #'angular_diffs.txt')

angles_data = {1:[],2:[],3:[],4:[]}

for line in file:
    line = line.strip()
    task = int(line.split(":")[0].split("_")[-1].split(".")[0])
    angles_data[task].append(float(line.split(":")[2]))

print "\\begin{center}"
print "\\begin{tabular}{|c|c|}"
print "\\hline"
print " Task & Average angular difference \\\\ \\hline"
for task in angles_data:
    angles = angles_data[task]
    if len(angles) < 1:
        break
    print task, " & ", round(sum(angles)/len(angles),3),"$\pm$", round(np.std(angles)/np.sqrt(len(angles)),3), "\\\\"
print "\\hline"
print "\\end{tabular}"
print "\\end{center}"
