#!/bin/python
import numpy as np
from numpy import linalg as LA
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


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

    def __init__(self, file_dir='data/subj63/63_16_1.data'): 
        f = open(file_dir)       
        self.data = {}
        self.trajectory = []
        self.fig, self.ax = plt.subplots() 
        for line in f:
            line.strip()
            line = line.split('#')
            dp = DataPoint(line)
            self.data[dp.time_step] = dp
            self.trajectory.append(np.array([dp.position[0],dp.position[1]])) 
        
    def plotObjects(self, object_points, color, size, ax):
        state_0 = (-2.8, 1.8)
        traj = []
        for point in object_points:
            state_x =  (math.floor(point[0]*10/2)*2)/10.0 #point[0] - 0.1 #
            state_y =  (math.floor(point[1]*10/2)*2)/10.0 #point[1] - 0.1 #
            circle2 = plt.Circle((state_x+0.1, state_y+0.1), size, color=color)
            ax.add_artist(circle2)
            state_idx = (state_0[1]-state_y)/0.2 * 28 + (state_x - state_0[0]) / 0.2
            if state_idx >= 0 and state_idx < 28*22:
                traj.append(int(state_idx))
        return traj
    
    def ProcessData(self):      
        self.targets = self.plotObjects(self.data[1].targets,'r',0.2134, self.ax)
        self.obstacles = self.plotObjects(self.data[1].obstacles,'b',0.1753, self.ax)
        self.path = self.plotObjects(self.data[1].pathpoints,'g', 0.05, self.ax)
        
    def Visualize(self,prefix="test"):
        fig = plt.gcf()
        ax = fig.gca()
        ax.xaxis.set_ticks(np.arange(-2.8, 2.8, 0.2))
        ax.yaxis.set_ticks(np.arange(-2.4, 2.0, 0.2))
        # change default range so that new circles will work
        ax.set_xlim((-2.8, 2.8))
        ax.set_ylim((-2.4, 2.0))
        ax.grid(color='g', linestyle='-', linewidth=1)
        traj = self.plotObjects(self.trajectory,'k', 0.05, self.ax )
        #plt.show()
        plt.savefig("birl_data/"+prefix+"_configuration.png", bbox_inches='tight')


    def OutputDomainFeatures(self,prefix="test"):
        outfile = open("birl_data/"+prefix+"_domain_features.txt","w")
        for state in self.targets:
            #print "stateFeatures["+str(state)+"][0] = 1.0;"
            outfile.write(str(state)+",0,1.0\n")
            if state >= 28:
                outfile.write(str(state-28)+",0,0.5\n")
            outfile.write(str(state+28)+",0,0.5\n")
           
            if not state % 28 == 0 :
                if state > 0:
                    outfile.write(str(state-1)+",0,0.5\n")
                if state > 28:
                    outfile.write(str(state-28-1)+",0,0.5\n")
                outfile.write(str(state+28-1)+",0,0.5\n")

            if not state % 28 == 27 :
                outfile.write(str(state+1)+",0,0.5\n")
                if state >= 28:
                    outfile.write(str(state-28+1)+",0,0.5\n")
                outfile.write(str(state+28+1)+",0,0.5\n")
            
        for state in self.obstacles:
            #print "stateFeatures["+str(state)+"][1] = 1.0;"
            outfile.write(str(state)+",1,0.5\n")
            if state >= 28:
                outfile.write(str(state-28)+",1,0.5\n")
            outfile.write(str(state+28)+",1,0.5\n")
            if not state % 28 == 0 :
                if state > 0:
                    outfile.write(str(state-1)+",1,0.5\n")
                if state > 28:
                    outfile.write(str(state-28-1)+",1,0.5\n")
                outfile.write(str(state+28-1)+",1,0.5\n")
            if not state % 28 == 27 :
                outfile.write(str(state+1)+",1,0.5\n")
                if state >= 28:
                    outfile.write(str(state-28+1)+",1,0.5\n")
                outfile.write(str(state+28+1)+",1,0.5\n")
            
        idx = 1
        for state in self.path:
            #print "stateFeatures["+str(state)+"][2] =" + str(idx/10.0) +";"
            outfile.write(str(state)+",2,"+ str(idx/10.0) +"\n")
            '''if state >= 28:
                outfile.write(str(state-28)+",2,"+ str(idx/10.0*0.5) +"\n")
            outfile.write(str(state+28)+",2,"+ str(idx/10.0*0.5) +"\n")
            if not state % 28 == 0 :
                if state > 0:
                    outfile.write(str(state-1)+",2,"+ str(idx/10.0*0.5) +"\n")
                if state > 28:
                    outfile.write(str(state-28-1)+",2,"+ str(idx/10.0*0.5) +"\n")
                outfile.write(str(state+28-1)+",2,"+ str(idx/10.0*0.5) +"\n")
            if not state % 28 == 27 :
                outfile.write(str(state+1)+",2,"+ str(idx/10.0*0.5) +"\n")
                if state >= 28:
                    outfile.write(str(state-28+1)+",2,"+ str(idx/10.0*0.5) +"\n")
                outfile.write(str(state+28+1)+",2,"+ str(idx/10.0*0.5) +"\n")'''
            idx += 1

    def OutputDemonstrations(self,prefix="test"):
        outfile = open("birl_data/"+prefix+"_demonstrations.txt","w")
        traj = self.plotObjects(self.trajectory,'k', 0.05, self.ax )
        demo = []
        width = 28
        height = 22
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
    parser.Visualize()

