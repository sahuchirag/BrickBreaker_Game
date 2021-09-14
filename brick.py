from config import *
from obj import *
from util import *

class Brick(Object):

    def __init__(self, type, pos, change=False):

        shape = listify("[ ]")
        self.__type = type  ## 0 => Normal, 1 => Unbreakable, 2 => Exploding, 3 => UFO
        self.__status = 3   ## Decreasing life/strength of brick from 3(max) to 0(disappear)
        self.__change = change 

        if(type == 3):
            shape = listify("   .-.   \n _/_0_\_ \n(_______)")
            self.__status = 50   ## Decreasing life/strength of brick from 100(max) to 0(disappear)
            brCol = [font['green'], bg['black']]

        else:
            brCol = [font['black'], bg[brickCol[self.__type][self.__status]]]

        super().__init__(shape, brCol, pos)

    def rainbow(self):
        if(self.__change):
            self.__status -= 1 

            if(self.__status == 0):
                self.__status = 3 

            self.setColor([self.getColor()[0], bg[brickCol[self.__type][self.__status]]])
            
    def hit(self, newStat):
        self.__status = newStat
        self.__change = False

        if(self.__type != 3):
            self.setColor([self.getColor()[0], bg[brickCol[self.__type][self.__status]]])

        if(not self.__status):
            self.destroy()

    def getType(self):
        return self.__type

    def getLife(self):
        return self.__status

    def collide(self, thru=False, fire=False):
        if((not self.__type or self.__type == 3) and not thru and not fire):
            self.hit(self.__status - 1)

        elif(self.__type == 2 or thru or fire):
            self.hit(0)
