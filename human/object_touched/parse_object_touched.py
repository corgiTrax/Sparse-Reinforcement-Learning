import numpy as np
from scipy import stats
import sys
import re
import matplotlib
import matplotlib.pyplot as plt

#if len(sys.argv) < 2:
#	print("Usage: python %s object_touched_?.txt" % sys.argv[0])
#	sys.exit(1)

fnames = ["mirl.txt", "random.txt", "binary.txt", "gamma01.txt", "gamma05.txt", "gamma099.txt"]

def mean_and_sem(fname, task_to_plot):
	print("Processing file %s" % fname)
	data_file = open(fname, 'r')

	#initiate 
	human_tars = [[],[],[],[]]
	human_obsts = [[],[],[],[]]
	agent_tars = [[],[],[],[]]
	agent_obsts = [[],[],[],[]]

	subj_task_msg = re.compile("Subject\s+(\d+)\s+Task\s+(\d+)")

	for line in data_file:
		if "Processing" in line:
			continue
		match_subj_task = subj_task_msg.match(line)
		if match_subj_task: # if a subject line
			subject, task = int(match_subj_task.group(1)), int(match_subj_task.group(2))
		else: # a data line
			task = task - 1
			data = line.split()
			for i in range(len(data)):
				data[i] = float(data[i])
			human_tars[task].append(data[0])
			human_obsts[task].append(data[1])
			agent_tars[task].append(data[2])
			agent_obsts[task].append(data[4])

	i = task_to_plot # task
	print("Task %d: " % (i + 1))
	human_tar_mean, human_tar_sem = np.mean(np.asarray(human_tars[i])), stats.sem(np.asarray(human_tars[i]))
	human_obst_mean, human_obst_sem = np.mean(np.asarray(human_obsts[i])), stats.sem(np.asarray(human_obsts[i]))
	agent_tar_mean, agent_tar_sem = np.mean(np.asarray(agent_tars[i])), stats.sem(np.asarray(agent_tars[i]))
	agent_obst_mean, agent_obst_sem = np.mean(np.asarray(agent_obsts[i])), stats.sem(np.asarray(agent_obsts[i]))
	print("Human target: %.2f +- %.2f" % (human_tar_mean, human_tar_sem))
	print("Human obst: %.2f +- %.2f" % (human_obst_mean, human_obst_sem))
	print("Agent target: %.2f +- %.2f" % (agent_tar_mean, agent_tar_sem ))
	print("Agent obst: %.2f +- %.2f" % (agent_obst_mean, agent_obst_sem))
	return [human_tar_mean, human_tar_sem, human_obst_mean, human_obst_sem], [agent_tar_mean, agent_tar_sem, agent_obst_mean, agent_obst_sem]

task = int(sys.argv[1])
humans, mirls = mean_and_sem(fnames[0], task)
humans, randoms = mean_and_sem(fnames[1], task)
humans, binarys = mean_and_sem(fnames[2], task)
humans, gamma01s = mean_and_sem(fnames[3], task)
humans, gamma05s = mean_and_sem(fnames[4], task)
humans, gamma099s = mean_and_sem(fnames[5], task)

#Now plot
ind = np.arange(2)
width = 0.1
offset = 0.1
fig, ax = plt.subplots()
randoms_plot = ax.bar(offset + ind, [randoms[0], randoms[2]], width, color='w', yerr=[randoms[1], randoms[3]], ecolor = 'black')
# bayesian IRL
gamma01s_plot = ax.bar(offset + ind + width * 2, [gamma01s[0], gamma01s[2]], width, color=(1,0.3,0.3), yerr=[gamma01s[1], gamma01s[3]], ecolor='black')
gamma05s_plot = ax.bar(offset + ind + width * 3, [gamma05s[0], gamma05s[2]], width, color='pink', yerr=[gamma05s[1], gamma05s[3]], ecolor = 'black')
gamma099s_plot = ax.bar(offset + ind + width * 4, [gamma099s[0], gamma099s[2]], width, color=(1.0,0.6,0.1), yerr=[gamma099s[1], gamma099s[3]], ecolor = 'black')
binarys_plot = ax.bar(offset + ind + width * 5, [binarys[0], binarys[2]], width, color='yellow', yerr=[binarys[1], binarys[3]], ecolor = 'black')
mirls_plot = ax.bar(offset + ind + width * 6, [mirls[0], mirls[2]], width, color='lightgreen', yerr=[mirls[1], mirls[3]], ecolor = 'black')
humans_plot = ax.bar(offset + ind + width * 7, [humans[0], humans[2]], width, color='lightblue', yerr=[humans[1], humans[3]], ecolor = 'black')

#add some text for labels, title and axes ticks
ax.set_ylabel('Number of Objects Touched', fontsize = 16)
ax.set_xticks(ind + width * 2)
ax.set_xticklabels((' '*10 + 'Target', ' '*15 + 'Obstacle'), fontsize = 16)
ax.set_ylim(0, 10)
#ax.set_xlim(0,3.9)
plt.legend((randoms_plot[0], gamma01s_plot[0], gamma05s_plot[0], gamma099s_plot[0], binarys_plot[0], mirls_plot[0], humans_plot[0]), \
	('Random', r'$\gamma=0.1$', r'$\gamma=0.5$', r'$\gamma=0.99$', 'Binary Reward', 'MIRL', 'Human'), ncol = 1, loc = 0, fontsize = 12) 

titles = ["Task1: Follow Path Only", "Task2: Path + Avoid Obstacles", "Task3: Path + Collect Targets", "Task4: Path + Obstacles + Targets"]
plt.title(titles[task], fontsize = 16)

plt.savefig("task" + str(task+1) + '.png', dpi = 300) 
plt.show()