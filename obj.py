import numpy as np

from config import *
from util import *

class Object:

    def __init__(self, shape, color, pos, active=True, vel=[0, 0]):
       self.__shape = shape 
       self.__color = color  # color[0] => fgcolor, color[1] => bgcolor
       self.__pos = pos      # pos = [x, y] of top left corner pixel/character of obj
       self.__vel = vel      # vel = [xvel, yvel]
       self.__active = active 
       self.__frame = 1

    def draw(self, grid):
        [xlen, ylen] = getShape(self.__shape)

        if(not self.__active):
            return

        for i in range(0, xlen):
            for j in range(0, ylen):
                grid[self.__pos[0] + i][self.__pos[1] + j] = self.__color[1] + self.__shape[i][j]

    def getDim(self):
        return np.shape(self.__shape)

    def getPos(self):
        return self.__pos[:]

    def getFrame(self):
        return self.__frame

    def setFrame(self, newFrame):
        self.__frame = newFrame

    def getVel(self):
        return self.__vel[:]

    def setVel(self, newVel):
        self.__vel = newVel

    def getColor(self):
        return self.__color[:]

    def getShape(self):
        return self.__shape[:]

    def setShape(self, shape):
        self.__shape = shape 

    def setColor(self, color):
        self.__color = color  

    def chckDown(self):
        # floor check
        if(self.__pos[0] + self.__vel[0] + self.getDim()[0] - 1 >= rows):
            return True

        return False

    def chckUp(self):
        # ceiling check
        if(self.__pos[0] + self.__vel[0] < 0):
            return True

        return False

    def chckWall(self):
        # side wall check
        if(self.__pos[1] + self.__vel[1] < 0 or self.__pos[1] + self.__vel[1] + self.getDim()[1] - 1 >= cols):
            return True

        return False

    def move(self, flag=0):
        # flag = 0 --> nothing, flag = 1 --> reflect, flag = 2 --> destroy for ceil 

        if(not self.chckWall()):
            self.__pos[1] = self.__pos[1] + self.__vel[1]

        elif(flag == 1):
            self.__vel[1] *= -1
            self.__pos[1] = self.__pos[1] + self.__vel[1]

        if(not self.chckUp() and not self.chckDown()):
            self.__pos[0] = self.__pos[0] + self.__vel[0]

        elif(flag == 1 and self.chckUp()):
            self.__vel[0] *= -1
            self.__pos[0] = self.__pos[0] + self.__vel[0]

        elif(flag == 2 and self.chckUp()):
            return True

        elif(self.chckDown()):
            self.destroy()
            return True

    def collide(self, newVel):                                            
        self.setVel(newVel)

    def getActive(self):
        return self.__active

    def activate(self, pos):
        self.__active = True
        self.__pos = pos[:]

    def destroy(self):
        self.__active = False
