import time

# from config import *
import config
from obj import *
from util import *
from ball import *

class Powerup(Object):

    def __init__(self, shape, pos, type):

        shape = listify(shape)
        self.__type = type
        self.__time = -1
        super().__init__(shape, [font['blue'], bg['black']], pos, False)
        self.setFrame(powFps)

    def getType(self):
        return self.__type

    def fall(self):
        self.setVel([jump, 0])

    def power(self, paddle, ball):
        self.setTime(time.time())

    def normal(self, paddle, ball):
        self.setTime(-1)

    def collide(self):
        self.destroy()
        self.setVel([1, 0])
        self.move()
        self.setVel([0, 0])

    def getTime(self):
        return self.__time

    def setTime(self, ttime):
        self.__time = ttime

class padExpand(Powerup):
    
    def __init__(self, pos):
        super().__init__("<=>", pos, 1)

    def power(self, paddle, balls):
        if(cols - paddle.getPos()[1] - paddle.getDim()[1] >= change):
            paddle.setShape(listify(" " * (paddle.getDim()[1] + change)))

class padShrink(Powerup):
    
    def __init__(self, pos):
        super().__init__(">=<", pos, 2)

    def power(self, paddle, balls):
        if(paddle.getDim()[1] > change):
            paddle.setShape(listify(" " * (paddle.getDim()[1] - change)))

class ballMul(Powerup):
    
    def __init__(self, pos):
        super().__init__("2xO", pos, 3)

    def power(self, paddle, balls):
        length = len(balls)

        for ind in range(0, length):
            tempos = balls[ind].getPos()
            temvel = balls[ind].getVel()

            if(not temvel[1]):
                temvel[1] += 1
            else:
                temvel[1] *= -1

            balls.append(Ball(tempos))
            balls[len(balls) - 1].setVel(temvel)

    def normal(self, paddle, balls, num):
        length = len(balls)

        for ind in range(length - 1, num - 1, -1):
            del balls[ind]

class ballFast(Powerup):
    
    def __init__(self, pos):
        super().__init__(">>>", pos, 4)

    def power(self, paddle, balls):
        for ball in balls:
            if(ball.getFrame() > 1):
                ball.setFrame(ball.getFrame() - 1)

class ballThru(Powerup):
    
    def __init__(self, pos):
        super().__init__("XXX", pos, 5)

    def power(self, paddle, balls):
        for ball in balls:
            ball.setThru(True)

class padGrab(Powerup):
    
    def __init__(self, pos):
        super().__init__("|_|", pos, 6)

    def power(self, paddle, balls):
        paddle.setStick(True)

class padShoot(Powerup):
    
    def __init__(self, pos):
        super().__init__("^_^", pos, 7)

    def power(self, paddle, balls):
        strg = "I" + " " * (paddle.getDim()[1] - 2) + "I"
        paddle.setColor([font['blue'], bg['purple']])
        paddle.setShape(listify(strg))

        paddle.setShoot(True)

class ballFire(Powerup):
    
    def __init__(self, pos):
        super().__init__("<O>", pos, 8)

    def power(self, paddle, balls):
        for ball in balls:
            ball.setFire(True)
