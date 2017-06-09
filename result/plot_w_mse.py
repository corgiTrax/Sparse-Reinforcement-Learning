import numpy as np
import matplotlib.pyplot as plt
import copy

files = []
files.append("MSE_nonsparse")
files.append("MSE_01")
#files.append("MSE_015")
#files.append("MSE_02")
files.append("MSE_025")
files.append("MSE_1")

datas = []
for file_ in files:
    temp_file = open(file_, 'r')
    data = []
    for line in temp_file:
        data.append(float(line))

    temp_file.close()
    datas.append(copy.deepcopy(data))

sample = []
for i in range(20):
    sample.append(20 * (i+1))

plt.gcf().set_size_inches(5,5)
plt.plot(sample,datas[0],'b',label = 'non-sparse')
plt.plot(sample,datas[1],'g',label = '$\lambda = 0.1$')
plt.plot(sample,datas[2],'r',label = '$\lambda = 0.25$')
plt.plot(sample,datas[3],'y',label = '$\lambda = 1$')

legend = plt.legend(loc = 'upper right')
plt.ylabel('Mean Squared Error of Rewards')
plt.xlabel('Number of Samples')
#plt.yticks(fontsize = 'x-large')
#plt.xticks(fontsize = 'x-large')
plt.savefig("sparse.png", dpi = 300)
#plt.show()
