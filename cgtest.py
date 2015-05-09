from graphics import *
import numpy as np


#window = GraphWin(width = 100, height = 100)
#ball = Circle(Point(20,20),10)
#
#colorList = ["black", "blue", "brown", "cyan", "gray", "green", "orange", "purple", "red", "white", "yellow"]
#ball.setFill(colorList[2])
#ball.draw(window)


class agent:
    def __init__(self,pos):
        self.pos = pos


a = [[1,2],[3,4]]
myAgent = agent([1,2])
print(myAgent.pos in a)
a.remove(myAgent.pos)
print(a)
print(myAgent.pos)


#raw_input("press enter to exit")
