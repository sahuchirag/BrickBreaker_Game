import numpy as np

from config import *

class Screen:

    def __init__(self):
        self.__grid = np.zeros((rows, cols), dtype = int)

    def clear(self):
        self.__grid = np.full((rows, cols), bg['black'] + ' ')
        print("\033[0;0H") #cursor to start(0, 0)

    def populate(self, obj):
       obj.draw(self.__grid) 

    def disp(self):

        for i in self.__grid: 
            for j in i:
                print(j, end='')
                         
            print("\n", end='')
