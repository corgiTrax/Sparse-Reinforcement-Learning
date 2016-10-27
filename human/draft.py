    def draw(self):
        ''' visualize data'''
        self.window = cg.GraphWin(title = "A Single Trial", width = ROOM_X * FACTOR + 50, height = ROOM_Z * FACTOR + 200)
        self.window.setBackground("gray")

        for time in range(self.timeSteps - 1): # exclude the last one which we can't compute action
            agentPos = utils.tile(self.agents[time][0])

            # draw all targets
            targetPics = []
            for targetPos in self.targets[time]:
                targetPic = cg.Circle(cg.Point(targetPos[0] * FACTOR, targetPos[1] * FACTOR), TAR_SIZE * FACTOR)
                targetPic.setFill("darkblue"); targetPic.setOutline("darkblue")
                targetPic.draw(self.window)
                targetPics.append(targetPic)
            # draw all obsts
            obstPics = []
            for obstPos in self.obsts[time]:
                topLeftPt = cg.Point(obstPos[0] * FACTOR - OBS_SIZE * FACTOR, obstPos[1] * FACTOR - OBS_SIZE * FACTOR)
                bottomRightPt = cg.Point(obstPos[0] * FACTOR + OBS_SIZE * FACTOR, obstPos[1] * FACTOR + OBS_SIZE * FACTOR)
                obstPic = cg.Rectangle(topLeftPt,bottomRightPt)
                obstPic.setFill("darkred"); obstPic.setOutline("darkred")
                obstPic.draw(self.window)
                obstPics.append(obstPic)
            # draw all paths
            pathPics = []
            for pathPos in self.paths[time]:
                pathPic = cg.Circle(cg.Point(pathPos[0] * FACTOR, pathPos[1] * FACTOR), TAR_SIZE/4 * FACTOR)
                pathPic.setFill("white"); pathPic.setOutline("white")
                pathPic.draw(self.window)
                pathPics.append(pathPic)
            # draw the elevator
            for elevPos in self.elevs[time]:
                elevPic = cg.Circle(cg.Point(elevPos[0] * FACTOR, elevPos[1] * FACTOR), TAR_SIZE * FACTOR)
                elevPic.setFill("yellow"); elevPic.setOutline("yellow")
                elevPic.draw(self.window)
            # draw agent path over time
            agentPos = self.agents[time][0]
            agentPic = cg.Circle(cg.Point(agentPos[0] * FACTOR, agentPos[1] * FACTOR), AGENT_SIZE * FACTOR)
            agentPic.setFill("green"); agentPic.setOutline("green")
            agentPic.draw(self.window)

            # click to go to next step
            if MOUSE: self.window.getMouse()
            for targetPic in targetPics: targetPic.undraw()
            for obstPic in obstPics: obstPic.undraw()
            for pathPic in pathPics: pathPic.undraw()


            if PATH_LOOKAHEAD:
            # determine which paths are for current time step
            # identify which paths are still ahead and store them
                nearest = utils.nearest_obj(agentPos, paths) 
                if self.startSide == 0: # start from the last path, 21, 20, ...,
                    # update passed_index
                    if pass_index - nearest > NUM_PATH_LOOKAHEAD + THROW_OUT: # do nothing, probably at another seg of path
                        pass
                    else: pass_index = nearest
                    for ct,path in enumerate(self.allPaths):
                        if pass_index - NUM_PATH_LOOKAHEAD < ct <= pass_index:
                            curPaths.append(cp.deepcopy(path))
                elif self.startSide == 1: # start from the first path, 0, 1, ..., 
                    # update passed_index
                    if nearest - pass_index > NUM_PATH_LOOKAHEAD + THROW_OUT: # do nothing, probably at another seg of path
                        pass
                    else: pass_index = nearest
                    for ct,path in enumerate(self.allPaths):
                        if pass_index <= ct < pass_index + NUM_PATH_LOOKAHEAD:
                            curPaths.append(cp.deepcopy(path))
                for pathPos in curPaths:
                    if utils.in_vcone(agentPos, agentAngle, pathPos):
                        for act in ACTIONS:
                            global_Q[act] += r * unit_r * (gamma ** utils.conseq(agentPos, utils.tile(pathPos), act, PATH_SIZE))





# in free_run visualization
        if not PILG:
            # 1.0 visualization of the environment
            self.window = cg.GraphWin(title = "A Single Trial", width = ROOM_X * FACTOR + 50, height = ROOM_Z * FACTOR + 200)
            self.window.setBackground("white")
            # draw all targets
            targetPics = []
            for targetPos in targets_init:
                targetPic = cg.Circle(cg.Point(targetPos[0] * FACTOR, targetPos[1] * FACTOR), TAR_SIZE * FACTOR)
                targetPic.setFill("darkblue"); targetPic.setOutline("darkblue")
                targetPic.draw(self.window)
                targetPics.append(targetPic)
            # draw all obsts
            obstPics = []
            for obstPos in obsts_init:
                topLeftPt = cg.Point(obstPos[0] * FACTOR - OBS_SIZE * FACTOR, obstPos[1] * FACTOR - OBS_SIZE * FACTOR)
                bottomRightPt = cg.Point(obstPos[0] * FACTOR + OBS_SIZE * FACTOR, obstPos[1] * FACTOR + OBS_SIZE * FACTOR)
                obstPic = cg.Rectangle(topLeftPt,bottomRightPt)
                obstPic.setFill("darkred"); obstPic.setOutline("darkred")
                obstPic.draw(self.window)
                obstPics.append(obstPic)
            # draw all paths
            pathPics = []
            for pathPos in paths_init:
                pathPic = cg.Circle(cg.Point(pathPos[0] * FACTOR, pathPos[1] * FACTOR), TAR_SIZE/4 * FACTOR)
                pathPic.setFill("gray"); pathPic.setOutline("gray")
                pathPic.draw(self.window)
                pathPics.append(pathPic)
            # draw the elevator
            for elevPos in elevs_init:
                elevPic = cg.Circle(cg.Point(elevPos[0] * FACTOR, elevPos[1] * FACTOR), TAR_SIZE * FACTOR)
                elevPic.setFill("yellow"); elevPic.setOutline("yellow")
                elevPic.draw(self.window)

            # 2.0
                agentLine = cg.Line(cg.Point(agentPos[0] * FACTOR, agentPos[1] * FACTOR), cg.Point(lastAgentPos[0] * FACTOR, lastAgentPos[1] * FACTOR))
                agentLine.setFill("green"); agentLine.setOutline("green"); agentLine.setWidth(0.3 * SIZE);
                agentLine.draw(self.window)
            
            # 3.0
            agentLine = cg.Line(cg.Point(agentPos[0] * FACTOR, agentPos[1] * FACTOR), cg.Point(lastAgentPos[0] * FACTOR, lastAgentPos[1] * FACTOR))
            agentLine.setFill("black"); agentLine.setOutline("black"); agentLine.setWidth(0.2 * SIZE);
            agentLine.draw(self.window)
        
        #saving
        self.window.postscript(file="image.eps")
        # Convert from eps format to gif format using PIL
        img = Image.open("image.eps")
        img.save(fname, "png")   

