from config import *
from obj import *
from util import *

class Paddle(Object):

    def __init__(self, pos):

        shape = listify(" " * padLen)
        self.__stick = True  # True => ball sticks to paddle, False => ball reflects
        self.__shoot = False
        super().__init__(shape, [font['black'], bg['white']], pos)

    def getStick(self):
        return self.__stick

    def setStick(self, stat):
        self.__stick = stat 

    def getShoot(self):
        return self.__shoot

    def setShoot(self, stat):
        self.__shoot = stat 

    def stickChck(self, ball):
        ballPos = ball.getPos()
        paddlePos = self.getPos()

        if(self.__stick and ballPos[0] == paddlePos[0] - 1 and ballPos[1] in range(paddlePos[1], paddlePos[1] + self.getDim()[1])):
            return True

        else:
            return False

    def keybrd(self, dirn, balls):
        # dirn = 0 --> right, dirn = 1 --> left 
        oldPos = self.getPos()
        oldVel = self.getVel()

        self.setVel([oldVel[0], pow(-1, dirn) * abs(jump)])
        self.move()
        self.setVel([0, 0])

        for ball in balls:
            ballPos = ball.getPos()

            if(oldPos != self.getPos() and self.stickChck(ball)):
                ball.setVel([oldVel[0], pow(-1, dirn) * abs(jump)])
                ball.move()
                ball.setVel([0, 0])

    def release(self, balls):
        for ball in balls:
            if(self.stickChck(ball)):
                ball.setVel([-1 * jump, ball.getOldVel()])

    def collide(self, ball):
        yvel = ball.getPos()[1] - self.getPos()[1] - (int)(self.getDim()[1] / 2)
        if(not self.__stick):
            ball.setVel([ball.getVel()[0], yvel])

        else:
            ball.setOldVel(yvel)
            ball.setVel([0, 0])
