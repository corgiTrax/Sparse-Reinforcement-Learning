import sys
sys.path.append('/home/zharuvrl/Projects/Sparse-Reinforcement-Learning/human')
from config import *
import world
from os import listdir
from os.path import isfile,join

direct = sys.argv[1]
files = [f for f in listdir(direct)]
# get all data files and build .dis files
dataFiles = []
for f in files:
    if f.find(".png") == -1 and f.find(".data") != -1 and f.find(".dis") == -1 and f.find(".fit") == -1:
        dataFiles.append(direct + f)
for f in dataFiles:
    print("Building .dis file for: " + f)
    newTrial = world.Trial(f)
    newTrial.build_irl_data()

# get all .data.dis files from subject data
files = [f for f in listdir(direct)]
disFiles = []
for f in files:
    if  f.find(".dis") != -1:
        disFiles.append(direct + f)
#print(disFiles)
# build crossfold .fit file for each
for disf in disFiles:
    print("Current file: " + disf)
    task = int(disf[-10]) # 1,2,3,4
    fitf = open(disf.replace("dis", "fit", 1), 'w')
    for disf2 in disFiles:
        if int(disf2[-10]) == task and disf2 != disf:
            print("Concatenating file: " + disf2)
            with open(disf2) as f:
                for line in f:
                    fitf.write(line)
    fitf.close()



