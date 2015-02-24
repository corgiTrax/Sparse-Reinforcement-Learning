'''modular reinforcement learning'''

from config import *
import agent

def calc_dists(agentPos, objPos, maze):
    '''for a module instance, for each action, calculate the 'x' variable in log likelihood function'''
    dists = [] 
    for act in ACTIONS:
        #suppose the agent really takes the current action act
        testAgent = agent.Agent(agentPos, maze)
        testAgent.move(act)
        #calc number of steps away from the object
        dist = abs(testAgent.pos[ROW] - objPos[ROW]) + abs(testAgent.pos[COL] - objPos[COL])
        dists.append(dist)
        del testAgent

    return dists

def calc_Qvalues(moduleClass, agentPos, objList, maze):
    '''given module class, agent position and instances' positions, calculate Q values'''
    Qvalues = []

    for objPos in objList:
        obj_Qvalue = []
        for act in ACTIONS:
            #suppose the agent really takes the current action act
            testAgent = agent.Agent(agentPos, maze)
            testAgent.move(act)

            #calc number of steps away from the object
            dist = abs(testAgent.pos[ROW] - objPos[ROW]) + abs(testAgent.pos[COL] - objPos[COL])

            if moduleClass == 'prize': Q = R_PRIZE * (GAMMA_PRIZE**dist)
            elif moduleClass == 'obstacle': Q = R_OBS * (GAMMA_OBS**dist)
            elif moduleClass == 'predator': Q = R_PRED * (GAMMA_PRED**dist)
            
            obj_Qvalue.append(Q)

            del testAgent

        Qvalues.append(obj_Qvalue)

    return Qvalues


def sumQ(Qvalues):
   '''given an array of Qvalues, perform sumQ algorithm'''
   sumed_Q = numpy.zeros(len(ACTIONS))
   for i in range(len(sumed_Q)):
       for j in range(len(Qvalues)):
           sumed_Q[i] += Qvalues[j][i]

   return sumed_Q


def softmax_act(Qvalues):
    '''Input: a vector of weights of actions
    Return: an action according to its softmax probability'''
    weights = py_copy.deepcopy(Qvalues)
    num_actions = len(weights)

    #map to exponential
    for i in range(num_actions):
        weights[i] = math.exp(weights[i])

    #normalize, get probability for each action
    total_weight = 0
    for i in range(num_actions):
        total_weight += weights[i]
    for i in range(num_actions):
        weights[i] = weights[i] / total_weight

    #calc cumulative probability
    cum_prob = numpy.zeros(num_actions + 1)
    cum_prob[0] = 0
    for i in range(num_actions):
        cum_prob[i+1] = cum_prob[i] + weights[i]

    #random seed
    seed = random.random()
    for i in range(num_actions):
        if (seed >= cum_prob[i] and seed < cum_prob[i+1]):
            action = i

    return action

