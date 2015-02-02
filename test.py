'''experiment file'''

import world
import moduleClass
import reinforceClass
import reinforceM1
import reinforceM2
import reinforceM3
import mathtool
import copy as py_copy
import graphics as graph
from config import *


#Read Qtables from each module
QtableM1 = mathtool.readQFromFile('Q1.txt',"M1")
QtableM2 = mathtool.readQFromFile('Q2.txt',"M2")
QtableM3 = mathtool.readQFromFile('Q3.txt',"M3")

testDataFile = open("ModuleCombination_greedy",'w')

for p_obs in ([pObstacle]):#([0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]):
    for p_chase in ([P_PREDATOR_CHASE]):#([0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]):
    
        #Performance criteria, for all trials
        totalReward = 0.0
        numSuccess = 0.0
        totalStepCountSuccess = 0.0
        totalPercPriceCollectFail = 0.0
        
        for trial in range(MAX_TRIAL):
            #generate a Maze
            testMaze = world.Maze(TESTR, TESTC, 'test', pObstacle = p_obs)
            if DRAW: testMaze.drawSelf(True)
            
            #Predator starts at (0,0)
            predators = []
            for i in range(NUM_PREDATOR):
                predator = reinforceClass.Predator([0,0])
                if DRAW: predator.drawSelf(testMaze.window, True)
                predators.append(predator)
            
            #Agent starts at middle
            myAgent = reinforceClass.Agent([int(TESTR/2),int(TESTC/2)])
            if DRAW: myAgent.drawSelf(testMaze.window,True)
            Captured = 0 #being captured by predator or not
            success = False #collect all prices
            stepCount = 0
            
            while (stepCount <= MAX_STEP and (Captured == 0) and (not success)):
                #print('Step count',stepCount)
            
                #Module Block #1: price
                if (NEAREST_PRICE_ONLY == False):
                    #Detect all prices within range, get their positions
                    pricesNear = world.findNearbyObj('price',myAgent.pos,TEST_VRANGE_M1,testMaze)
                    #Initialize one module for each price
                    priceModules = []
                    #Each module measure its own state, suggested action, flatness, and weight
                    for i in range(len(pricesNear)):
                        state = reinforceM1.stateMapping_M1(myAgent.pos,pricesNear[i])
                        priceModules.append(moduleClass.Module(QtableM1,state))
            
                if (NEAREST_PRICE_ONLY == True):    
                    #Detect nearest price
                    priceNearest = world.findNearestPrice(myAgent.pos,testMaze)
        #            print("Agent is at: ", myAgent.pos)
        #            print("Currently pursuing: ", priceNearest)
                    priceModules = []
                    state = reinforceM1.stateMapping_M1(myAgent.pos,priceNearest)
                    priceModules.append(moduleClass.Module(QtableM1,state))
                    if DRAW: testMaze.drawTargetPrice(priceNearest)
            
                #Module Block #2: obstacles
                #Detect all obstacles within range, get their positions
                obstaclesNear = world.findNearbyObj('obstacle',myAgent.pos,TEST_VRANGE_M2,testMaze)
                #Initialize one module for each obstacle
                obstacleModules = []
                #Each module measure its own state, suggested action, flatness, and weight
                for i in range (len(obstaclesNear)):
                    state = reinforceM2.stateMapping_M2(myAgent.pos,obstaclesNear[i])
                    newModule = moduleClass.Module(QtableM2,state)
                    obstacleModules.append(newModule)
            
                #Module Block #3: predator
                predatorModules = []
                for i in range(len(predators)):
                    if (abs(predators[i].pos[0] - myAgent.pos[0]) <= TEST_VRANGE_M3 and abs(predators[i].pos[1] - myAgent.pos[1]) <= TEST_VRANGE_M3):
                        predatorModules.append(moduleClass.Module(QtableM3,reinforceM3.stateMapping_M3(myAgent.pos,predators[i].pos)))
            
                #Combine all suggested action by their weight, determine global action
                allModules = []
                allModules = priceModules + obstacleModules + predatorModules    
                scores = moduleClass.vote(allModules)
                action = moduleClass.decideAct(scores)
            #    for i in range(len(priceModules)):
            #        print('Executing price module:',i,'Price pos:',reinforceM1.stateMappingInverse_M1(priceModules[i].state,myAgent.pos),'Q values',priceModules[i].Qvalues,'action:',priceModules[i].optimalAct,'sd weight:',priceModules[i].weight)
            #    for i in range(len(obstacleModules)):
            #        print('Executing obstacle module:',i,'Obs pos:',reinforceM2.stateMappingInverse_M2(obstacleModules[i].state,myAgent.pos),'Q values',obstacleModules[i].Qvalues,'action:',obstacleModules[i].optimalAct,'weight:',obstacleModules[i].weight)
            #    for i in range(len(predatorModule)):
            #        print('Executing predator module:',0,'predator pos:',predator.pos,'Q values',predatorModule[0].Qvalues,'action:',predatorModule[0].optimalAct,'weight:',predatorModule[0].weight)
            #     
            #    print('GMQ total score',scores,'action',action)
            
                #move one step only when mouse clicks
                if MOUSE: testMaze.window.getMouse()
                
                #agent takes action, and compute reward
                for i in range(len(predators)):
                    predators[i].move(predator.chase(myAgent.pos, p_chase),testMaze)
                myAgent.move(action,testMaze)
                for i in range(len(predators)):
                    Captured += (myAgent.pos == predators[i].pos)
                
                #Calculate cumulative reward
                myAgent.cumReward += testMaze.calc_reward(myAgent.pos)#calc_reward function also remove prices from maze price list
                if (Captured > 0): myAgent.cumReward -= R_PREDATOR
            
                #Visualization
                if DRAW:
                    testMaze.drawSelf(False)   
                    myAgent.drawSelf(testMaze.window, False)
                    for i in range(len(predators)):
                        predators[i].drawSelf(testMaze.window,False)
                
                stepCount +=1
        #        print('step:',stepCount)
                
                if len(testMaze.prices) == 0:
                #    print("task success")
                    success = True
        
        #    print("trial:",trial,"success?",success,"steps",stepCount,"cumReward",myAgent.cumReward)
            
            totalReward += myAgent.cumReward
            numSuccess += success
            if (success): totalStepCountSuccess += stepCount
            if (not success): totalPercPriceCollectFail += (1.0  - (len(testMaze.prices)/float(testMaze.originalNumPrices))) 
            
            #print(trial)
        
        #Final result
        avgReward = totalReward/MAX_TRIAL
        successRate = numSuccess/MAX_TRIAL
        if numSuccess != 0:
            avgSteps = totalStepCountSuccess/numSuccess
        else:
            avgSteps = MAX_STEP
        if (MAX_TRIAL - numSuccess != 0): 
            avgPrice = totalPercPriceCollectFail/(MAX_TRIAL - numSuccess)
        else:
            avgPrice = 1.0

        testDataFile.write(str(p_obs) + ' ' +  str(p_chase + 0.25) + ' ' +  str(avgReward) + ' ' + str(successRate) + ' ' + str(avgSteps) + ' ' + str(avgPrice) + '\n')

#Hold graph window
#raw_input("Press enter to exit")

 
########################## Repository ######################
#
#
#
#
#
#

