"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt
import ast
import config

n_groups = 2

def parseFiles(filename, xAxis, perTrial):
  means = []
  cis = []

  for xId in xrange(len(xAxis)):
    data = []
    for trialId in xrange(perTrial):
      condorId = xId * perTrial + trialId
      try:
        with open(filename + "." + str(condorId), 'r') as f:
          datum = ast.literal_eval(f.read())
          data.append(datum)
      except:
        print "issue in processing ", filename, condorId
    means.append(np.mean(data))
    cis.append(1.96 * np.std(data) / np.sqrt(len(data)))
    
    print data
  
  plt.errorbar(xAxis, means, cis)

parseFiles("eval_modular_vs_bayes/grid_modular_out", config.BUDGET_SIZES, 10)
parseFiles("eval_modular_vs_bayes/grid_bayes_out", config.BUDGET_SIZES, 10)

plt.gcf().set_size_inches(5,4)
plt.xlabel('Number of Samples')
plt.ylabel('Policy Agreement')
plt.axis([0, 110, 0.5, 1])
plt.legend(["Modular IRL", "Bayesian IRL"], "lower right")
plt.savefig("grid_modular_vs_bayes.png")
plt.close()
