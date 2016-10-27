# normalize weights
import sys
from os import listdir
from os.path import isfile,join

# get file
direct = sys.argv[1]
fns = [f for f in listdir(direct)]
fns.sort()
for fn in fns:
#    print(fn)
    f = open(direct+fn,'r')
    weights = []
    gammas = []
    for n, line in enumerate(f):
        if n % 2 == 0: # weight
            weights.append(float(line))
        else:
            gammas.append(float(line))
    
    sumW = sum(weights)
    for i in range(len(weights)):
        weights[i] /= sumW
    
    print("Results for file: " + fn)
    print("Normalized weights are: ")
    for w in weights:
        print("{0:0.2f}".format(w))
    print("\nDiscount factors are: ")
    for g in gammas:
        print("{0:0.2f}".format(g))
    
    f.close()

