import numpy as np
import matplotlib.pyplot as plt
import copy

files = []
files.append("MSE_nonsparse")
files.append("MSE_01")
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

plt.gcf().set_size_inches(5,4)
plt.plot(sample,datas[0],'b--o',label = '$\delta^2 = 0$')
plt.plot(sample,datas[1],'y--v',label = '$\delta^2 = 0.1$')
plt.plot(sample,datas[2],'r--p',label = '$\delta^2 = 0.25$')
plt.plot(sample,datas[3],'g--D',label = '$\delta^2 = 1$')

legend = plt.legend(loc = 'upper right', fontsize='xx-large')
plt.ylabel('Weight MSE', fontsize = 'x-large')
plt.xlabel('Number of Samples', fontsize = 'x-large')
plt.yticks(fontsize = 'x-large')
plt.xticks(fontsize = 'x-large')

plt.show()
