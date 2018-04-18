#!/bin/python
import numpy as np
from numpy import linalg as LA
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import random

GRID_CELL_SIZE = 0.2
GRID_LENGTH = 32
GRID_HEIGHT = 24
state_0 = (-3.2, 2.4)

class DataPoint(object):
    
    def __init__(self, input_data):
        self.time_step = int(input_data[0])
        self.position = tuple(float(e) for e in input_data[1].split(','))
        self.targets = []
        targets_data = [e for e in input_data[2].split(';')]
        for target in targets_data:
            t = target.split(',')
            if len(t) == 2:
                self.targets.append((float(t[0]),float(t[1])))
        self.obstacles = []
        obstacles_data = [e for e in input_data[3].split(';')]
        for obstacle in obstacles_data:
            t = obstacle.split(',')
            if len(t) == 2:
                self.obstacles.append((float(t[0]),float(t[1])))
        self.pathpoints = []
        pathpoint_data = [e for e in input_data[4].split(';')]
        for pathpoint in pathpoint_data:
            t = pathpoint.split(',')
            if len(t) == 2:
                self.pathpoints.append((float(t[0]),float(t[1])))
        self.destination = tuple(float(e) for e in input_data[5].split(','))

    def display(self):
        print "\ndata point:"  , self.time_step
        print "position:"    , self.position
        print "destination:" , self.destination
        print "targets: "    , self.targets
        print "obstacles:"   , self.obstacles
        print "pathpoints:"  , self.pathpoints

  

class HumanDataParser():

    def __init__(self, file_dir='data/subj32/32_16_1.data'): 
        plt.axes().set_aspect('equal', 'datalim')
        f = open(file_dir)       
        self.data = {}
        self.trajectory = []
        self.fig, self.ax = plt.subplots() 
        self.destination = None
        self.state_centers = {}
        for line in f:
            line.strip()
            line = line.split('#')
            dp = DataPoint(line)
            self.data[dp.time_step] = dp
            self.trajectory.append(np.array([dp.position[0],dp.position[1]])) 
            if self.destination == None:
                self.destination = dp.destination
        for state in range(GRID_LENGTH*GRID_HEIGHT):
            self.state_centers[state] = (state % GRID_LENGTH * GRID_CELL_SIZE + state_0[0],-state // GRID_LENGTH * GRID_CELL_SIZE + state_0[1])
        
    def plotObjects(self, object_points, color, size, ax, rectangle = False):
        
        traj = []
        for point in object_points:
            state_x =  point[0] # - GRID_CELL_SIZE/2 #(math.floor(point[0]*10/2)*2)/10.0 #
            state_y =  point[1] # - GRID_CELL_SIZE/2 #(math.floor(point[1]*10/2)*2)/10.0 #
            if rectangle:
                rect = plt.Rectangle((state_x, state_y),size*2,size*2, color=color, fill=True)
                ax.add_patch(rect)
            else:
                circle2 = plt.Circle((state_x, state_y), size, color=color)
                ax.add_artist(circle2)
            state_idx = (state_0[1]-state_y)/GRID_CELL_SIZE * GRID_LENGTH + (state_x - state_0[0]) / GRID_CELL_SIZE
            if state_idx >= 0 and state_idx < GRID_LENGTH*GRID_HEIGHT:
                traj.append(int(state_idx)) 
        return traj
    
    def getAction(self, action):
        if action == 0: #up
                return (0,-0.08)
        if action == 1: #down
                return (0,0.08)
        if action == 2: #left
                return (-0.08,0)
        if action == 3: #right
                return (0.08,0)
        if action == 4: #up_left
                return (-0.08,-0.08)
        if action == 5: #up_right
                return (0.08,-0.08)
        if action == 6: #down_left
                return (-0.08,0.08)
        if action == 7: #down_right
                return (0.08,0.08)
        else:
                return (0.0,-0.08)

    def plotActions(self, points, color, size, ax):
        traj_x = []
        traj_y = []
        targets_collected = {}
        obstacles_collected = {}
        for point in points:
            state_x = point[0] % GRID_LENGTH * GRID_CELL_SIZE + state_0[0]
            state_y = - point[0] // GRID_LENGTH * GRID_CELL_SIZE + state_0[1]
            traj_x.append(state_x+0.15-0.1*random.random())
            traj_y.append(state_y+0.15-0.1*random.random())
            #circle2 = plt.Circle((state_x+0.1, state_y+0.1), size, color=color)
            #ax.add_artist(circle2)
            action = self.getAction(point[1])
            #ax.arrow(state_x+0.1,state_y+0.1, action[0],action[1], width=0.05, head_width=0.08, head_length=0.08, color=color)
            traj_x.append(state_x+0.15-0.1*random.random()+action[0])
            traj_y.append(state_y+0.15-0.1*random.random()+action[1])
            for target in self.data[1].targets:
                if math.sqrt((state_x - target[0])**2 + (state_y - target[1])**2) <= 0.2134+0.14:
			targets_collected[target] = 1
            for target in self.data[1].obstacles:
                if math.sqrt((state_x - target[0])**2 + (state_y - target[1])**2) <= 0.1753+0.14:
			obstacles_collected[target] = 1
        #plt.plot(traj_x,traj_y,color='g',alpha=0.2, linewidth=0.28)
        return len(targets_collected), len(obstacles_collected)

    def ProcessData(self, prefix="test"):      
        self.targets = self.plotObjects(self.data[1].targets,'darkblue',0.2134, self.ax)
        self.obstacles = self.plotObjects(self.data[1].obstacles,'darkred',0.1753, self.ax, rectangle=True)
        self.path = self.plotObjects(self.data[1].pathpoints,'tab:gray', 0.05, self.ax)
        outfile = open("birl_data/"+prefix+"_objects.txt","w")
        outfile.write("targets: "+",".join([str(target) for target in self.data[1].targets])+'\n')
        outfile.write("obstacles: "+",".join([str(obstacle) for obstacle in self.data[1].obstacles])+'\n')
        outfile.write("path: "+",".join([str(pathpoint) for pathpoint in self.data[1].pathpoints])+'\n')
        outfile.write("destination: "+ str(self.destination)+'\n')
        outfile.close()
        
    def Visualize(self,prefix="test"):
        fig = plt.gcf()
        ax = fig.gca()
        ax.xaxis.set_ticks(np.arange(state_0[0], state_0[0] + GRID_CELL_SIZE*(GRID_LENGTH+1), GRID_CELL_SIZE))
        ax.yaxis.set_ticks(np.arange(state_0[1]- GRID_CELL_SIZE*(GRID_HEIGHT+1), state_0[1], GRID_CELL_SIZE))
        # change default range so that new circles will work
        ax.set_xlim(state_0[0], state_0[0] + GRID_CELL_SIZE*(GRID_LENGTH+1))
        ax.set_ylim(state_0[1]- GRID_CELL_SIZE*(GRID_HEIGHT+1), state_0[1])
        ax.grid(color='g', linestyle='-', linewidth=1)
        traj = self.plotObjects(self.trajectory,'k', 0.05, self.ax )
        #plt.show()
        plt.savefig("birl_data/"+prefix+"_configuration.png", bbox_inches='tight')

    def PlotTrajectory(self, trajs, prefix='test' , show=False):
        #fig = plt.gcf()
        #ax = fig.gca()
       
        #ax.xaxis.set_visible(False)
        #ax.yaxis.set_visible(False)
        #circle = plt.Circle((self.destination[0], self.destination[1]), 0.3, color='y', alpha=0.8)
        #ax.add_artist(circle)
        
        trajectory_x = []
        trajectory_y = []
        for point in self.trajectory:
            trajectory_x.append(point[0])
            trajectory_y.append(point[1])
        #self.plotObjects(self.trajectory,'k', 0.05, self.ax )
        #plt.plot(trajectory_x,trajectory_y, color='k')
        targets = 0
        obstacles = 0
        for traj in trajs:
            curr_targets, curr_obstacles = self.plotActions(traj,'y', 0.05, self.ax )
            targets += curr_targets
            obstacles += curr_obstacles
        #if show:
            #plt.show()
        #else:
            #plt.axis('off')
            #plt.savefig("birl_data/"+prefix+"_traj.png", bbox_inches='tight', format='png', dpi=200)
        return targets/len(trajs), obstacles/len(trajs)
        

    def OutputDomainFeatures(self,prefix="test"):
        outfile = open("birl_data/"+prefix+"_domain_features.txt","w")
        features = {} # state: [target,obstacles,path]
        for state in range(GRID_LENGTH*GRID_HEIGHT):
            features[state] = [0.0,0.0,0.0]

        for target in self.data[1].targets:
            for state in range(GRID_LENGTH*GRID_HEIGHT):
                s_x, s_y = self.state_centers[state]
                dist = math.sqrt((s_x - target[0])**2 + (s_y - target[1])**2)
                features[state][0] += max(0, (0.2134 - dist) / 0.2134 * 2)

        for obstacle in self.data[1].obstacles:
            for state in range(GRID_LENGTH*GRID_HEIGHT):
                s_x, s_y = self.state_centers[state]
                dist = math.sqrt((s_x - obstacle[0])**2 + (s_y - obstacle[1])**2)
                features[state][1] += max(0, (0.1753 - dist) / 0.1753 * 2)

        for pp in self.data[1].pathpoints:
            for state in range(GRID_LENGTH*GRID_HEIGHT):
                s_x, s_y = self.state_centers[state]
                dist = math.sqrt((s_x - pp[0])**2 + (s_y - pp[1])**2)
                features[state][2] += max(0, (0.2 - dist) / 0.2 * 2)

        for state in range(GRID_LENGTH*GRID_HEIGHT):
            for i in range(3):
               if not features[state][i] == 0:
                   outfile.write(str(state)+","+str(i)+","+str(features[state][i])+"\n")


    def OutputDemonstrations(self,prefix="test"):
        outfile = open("birl_data/"+prefix+"_demonstrations.txt","w")
        traj = self.plotObjects(self.trajectory,'k', 0.05, self.ax )
        demo = []
        width = GRID_LENGTH
        height = GRID_HEIGHT
        for pt in range(len(traj)-1):
            action = 0 # UP
            v = self.trajectory[pt+1] - self.trajectory[pt]
            alpha = math.atan2(v[1], v[0])
            k = alpha / (math.pi/8)
            if -1 < k <= 1:
                action = 3
            elif 1 < k <= 3:
                action = 5
            elif 3 < k <= 5:
                action = 0
            elif 5 < k <= 7:
                action = 4
            elif 7 < k or k <= -7:
                action = 2
            elif -3 < k <= -1:
                action = 7
            elif -5 < k <= -3:
                action = 1
            elif -7 < k <= -5:
                action = 6                   
            demo.append((traj[pt],action))
            
        for sa in demo:
            #print "good_demos.push_back(make_pair"+str(sa)+");"
            outfile.write(str(sa[0])+","+str(sa[1])+"\n")
    

if __name__ == '__main__':
    parser = HumanDataParser()
    parser.ProcessData()
    #parser.Visualize()
    fh = open('baseline_birl/outfile.txt','r')
    trajectories = []
    for line in fh:
        line = line.strip()
        if line.startswith("["):
            trajectories.append(eval(line))
    parser.PlotTrajectory(trajectories, show=True)


