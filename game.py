"""Defining input class."""
import sys
import termios
import tty
import signal
import os 
import time
import random
import numpy as np

from config import *
from screen import *
from brick import *
from paddle import *
from ball import *
from powerup import *
from bullet import *
from input import *

class Game:

    def __init__(self, lives, score, lvl):
        self.__input = KBHit()
        self.__screen = Screen()
        self.__start = time.time()
        if(lvl != lvlnum):
            self.__brickCtr = (int)((cols - 4) / (3 * (lvlnum - lvl)))
        self.__bricks = []
        self.__powers = []
        self.__explode = []
        self.__bullets = []
        self.__bombs = []
        self.__lifeRec = True
        self.__moveBr = 0
        self.__spawn = False

        self.__lives = lives
        self.__score = score
        self.__lvl = lvl
        # np.empty((6, self.__brickCtr))

        for i in range(0, 6):
            if(self.__lvl == lvlnum):
                break

            self.__bricks.append([])
            for j in range(0, self.__brickCtr):
                if(i == j):
                    self.__bricks[i].append(Brick(1, [2 + i, 2 + 3 * (lvlnum - lvl) * j]))
                # placing unbreakable bricks

                elif(self.__brickCtr - 1 - j == i):
                    self.__bricks[i].append(Brick(1, [2 + i, 2 + 3 * (lvlnum - lvl) * j]))
                # placing unbreakable bricks

                elif(i == j - 1):
                    self.__bricks[i].append(Brick(2, [2 + i, 2 + 3 * (lvlnum - lvl) * j]))
                # placing exploding bricks

                elif(self.__brickCtr - 2 - j == i):
                    self.__bricks[i].append(Brick(2, [2 + i, 2 + 3 * (lvlnum - lvl) * j]))
                # placing exploding bricks

                elif(j == (int)(self.__brickCtr / 2)):
                    self.__bricks[i].append(Brick(0, [2 + i, 2 + 3 * (lvlnum - lvl) * j], True))

                else:
                    self.__bricks[i].append(Brick(0, [2 + i, 2 + 3 * (lvlnum - lvl) * j]))
                # placing normal bricks
        
                # placing powerups 
                #NOTE: Always append padShoot after padExpand and padShrink for shape purposes
        if(lvl != lvlnum):
            self.__powers.append(padExpand(self.__bricks[random.randint(0, 5)][random.randint(0, self.__brickCtr - 1)].getPos()))
            self.__powers.append(padShrink(self.__bricks[random.randint(0, 5)][random.randint(0, self.__brickCtr - 1)].getPos()))
            self.__powers.append(ballMul(self.__bricks[random.randint(0, 5)][random.randint(0, self.__brickCtr - 1)].getPos()))
            self.__powers.append(ballFast(self.__bricks[random.randint(0, 5)][random.randint(0, self.__brickCtr - 1)].getPos()))
            self.__powers.append(ballThru(self.__bricks[random.randint(0, 5)][random.randint(0, self.__brickCtr - 1)].getPos()))
            self.__powers.append(padGrab(self.__bricks[random.randint(0, 5)][random.randint(0, self.__brickCtr - 1)].getPos()))
            self.__powers.append(padShoot(self.__bricks[random.randint(0, 5)][random.randint(0, self.__brickCtr - 1)].getPos()))
            self.__powers.append(ballFire(self.__bricks[random.randint(0, 5)][random.randint(0, self.__brickCtr - 1)].getPos()))

        if(self.__lvl == lvlnum):
            self.__bricks.append([])
            self.__bricks[0].append(Brick(3, [1, (int)(cols / 2) - 4]))

        self.__paddle = Paddle([rows - 2, (int)(cols / 2) - 2])
        self.__balls = [Ball([self.__paddle.getPos()[0] - 1, self.__paddle.getPos()[1] + (int)(self.__paddle.getDim()[1] / 2)])]
        self.__ballCtr = 1

    def spawnBricks(self, ufo):
        for i in range(1, 3 + 1):
            if(len(self.__bricks) > i):
                self.__bricks[i] = []

            else:
                self.__bricks.append([])

            for j in range(0, cols - 3, 3):
                self.__bricks[i].append(Brick(0, [ufo.getPos()[0] + ufo.getDim()[0] + i - 1, j]))
                # placing normal bricks

    def findPup(self, type):
        for x in self.__powers:
            if(x.getType() == type):
                return x

    def bossMove(self):
        ufo = self.__bricks[0][0]
        pad = self.__paddle

        if(ufo.getType() != 3):
            return 

        ufoMid = (int)(ufo.getPos()[1] + ufo.getDim()[1] / 2)
        if(pad.getPos()[1] + pad.getDim()[1] - 1 < ufoMid):
            ufo.setVel([0, -1])
            ufo.move()
            ufo.setVel([0, 0])

        elif(pad.getPos()[1] > ufoMid):
            ufo.setVel([0, 1])
            ufo.move()
            ufo.setVel([0, 0])

    def handle_input(self, txt):
        if(txt == 'a' or txt == 'A'):
            self.__paddle.keybrd(1, self.__balls)

        elif(txt == 'd' or txt == 'D'):
            self.__paddle.keybrd(0, self.__balls)

        elif(txt == ' '):
            self.__paddle.release(self.__balls)
            self.__lifeRec = False
            
            retPow = self.findPup(6)
            if(retPow and retPow.getTime() == -1):
                self.__paddle.setStick(False)

        if(txt == 'n' or txt == 'N'):
            return True

        elif(txt == 'q'):
            print("\033[?25h")
            quit()

    def verticalCol(self, pos1, pos2, dim1, dim2, fix=False): 
        if(set(range(pos1[0], pos1[0] + dim1[0])) & set(range(pos2[0], pos2[0] + dim2[0]))):
            if(fix and set(range(pos1[1], pos1[1] + dim1[1])) & set(range(pos2[1], pos2[1] + dim2[1]))):
                return True 
            else:
                return False

        return True 

    def findBrickByPos(self, pos):
        for m in range(0, len(self.__bricks)):
            for n in range(0, len(self.__bricks[m])):
                if(self.__bricks[m][n].getPos() == pos):
                    if(not self.__bricks[m][n].getActive()):
                        return None
                    return self.__bricks[m][n]

    def findBricks(self, brick, fire=False):
        posit = brick.getPos()
        dim = brick.getDim()

        if(brick.getType() == 2 or fire):
            for a in range(posit[0] - 1 * dim[0], posit[0] + 2 * dim[0], dim[0]):
                for b in range(posit[1] - 1 * dim[1], posit[1] + 2 * dim[1], dim[1]):
                    if(a == posit[0] and b == posit[1]):
                        continue

                    ret = self.findBrickByPos([a, b])
                    if(ret != None):
                        self.__explode.append(ret)

    def explosion(self):
        length = len(self.__explode)
        for z in range(0, length):
            self.findBricks(self.__explode[z])
            self.__explode[z].collide(True)
            self.__score += points

            for k in range(0, len(self.__powers)):
                if(self.__powers[k].getPos() == self.__explode[z].getPos() and not self.__powers[k].getActive()):
                    self.__powers[k].activate(self.__powers[k].getPos())
                    self.__powers[k].setVel([-2, 0])

        for z in range(0, length):
            del self.__explode[0]

    def colChck(self, pos1, dim1, pos2, dim2):
        if(set(range(pos1[0], pos1[0] + dim1[0])) & set(range(pos2[0], pos2[0] + dim2[0]))):
            if(set(range(pos1[1], pos1[1] + dim1[1])) & set(range(pos2[1], pos2[1] + dim2[1]))):
                return True

        return False

    def collision(self, obj, flags):
        # obj always moving obj such as ball or powerup
        # flags[0] --> paddle interaction type, flags[1] --> brick interaction type

        p1 = np.array(obj.getPos()[:])
        v1 = np.array(obj.getVel()[:])
        dim1 = obj.getDim()[:]

        sign = [1, 1]

        if(v1[0]):
            sign[0] = (int)(v1[0] / abs(v1[0]))

        if(v1[1]):
            sign[1] = (int)(v1[1] / abs(v1[1]))

        for r in range(0, abs(v1[0]) + 1):
            for c in range(0, abs(v1[1]) + 1):
                cr = p1[0] + r * sign[0]
                cc = p1[1] + c * sign[1]
                pos1 = [cr, cc]

                if(cr == p1[0] and cc == p1[1]):
                    continue

                if(flags[0] == 1):
                    pos2 = np.array(self.__paddle.getPos()) + np.array(self.__paddle.getVel())
                    dim2 = self.__paddle.getDim()

                    if(self.colChck(pos1, dim1, pos2, dim2)):
                        if(self.verticalCol(obj.getPos(), self.__paddle.getPos(), dim1, dim2)):
                            self.__paddle.collide(obj)
                            obj.collide([-1 * obj.getVel()[0], obj.getVel()[1]])
                            if(time.time() - self.__start >= timeLim):
                                self.__moveBr += 1

                            return

                elif(flags[0] == 2):

                    pos2 = np.array(self.__paddle.getPos()) + np.array(self.__paddle.getVel())
                    dim2 = self.__paddle.getDim()

                    if(self.colChck(pos1, dim1, pos2, dim2)):
                        if(self.verticalCol(obj.getPos(), self.__paddle.getPos(), dim1, dim2)):
                            return 1

                if(flags[1]):

                    for i in range(0, len(self.__bricks)):
                        for j in range(0, len(self.__bricks[i])):
                            if(not self.__bricks[i][j].getActive()):
                                continue

                            pos2 = np.array(self.__bricks[i][j].getPos()) + np.array(self.__bricks[i][j].getVel())
                            dim2 = self.__bricks[i][j].getDim()

                            if(self.colChck(pos1, dim1, pos2, dim2)):

                                thru = False
                                fire = False

                                if(flags[1] == 1):
                                    thru = obj.getThru()
                                    fire = obj.getFire()

                                self.findBricks(self.__bricks[i][j], fire)
                                self.__bricks[i][j].collide(thru, fire)
                                btype = self.__bricks[i][j].getType()
                                blife = self.__bricks[i][j].getLife()

                                if(btype == 3 and (blife == spawn1 or blife == spawn2)):
                                    self.__spawn = True

                                if(not self.__bricks[i][j].getActive()):
                                    self.__score += points
                                    if(self.__bricks[i][j].getType() == 3):
                                        self.__score += 100 * points


                                    for k in range(0, len(self.__powers)):
                                        if(self.__powers[k].getPos() == self.__bricks[i][j].getPos() and not self.__powers[k].getActive()):
                                            self.__powers[k].activate(self.__powers[k].getPos())
                                            self.__powers[k].setVel(obj.getVel())

                                if(thru or fire):
                                    continue

                                if(flags[1] == 2):
                                    return True

                                elif(self.verticalCol(obj.getPos(), self.__bricks[i][j].getPos(), dim1, dim2, self.__bricks[i][j].getType() == 3)):
                                    obj.collide([-1 * obj.getVel()[0], obj.getVel()[1]])
                                    return

                                else:
                                    obj.collide([obj.getVel()[0], -1 * obj.getVel()[1]])
                                    return

        return 0 

    def activation(self):
        for i in range(0, len(self.__powers)):
            if(self.__powers[i].getTime() != -1):
                if(self.__powers[i].getType() == 3): 
                    continue

                self.__powers[i].power(self.__paddle, self.__balls)

    def reset(self):
        self.__paddle.setColor([font['black'], bg['white']])
        self.__paddle.setShape(listify(" " * padLen))
        if(not self.__lifeRec):
            self.__paddle.setStick(False)
        self.__paddle.setShoot(False)

        for b in range(0, len(self.__balls)):
            self.__balls[b].setFrame(ballFps)
            self.__balls[b].setThru(False)
            self.__balls[b].setFire(False)

    def padPowCol(self):
        temp = []
        for i in range(0, len(self.__powers)):
            if(not self.__powers[i].getActive()):
                continue

            ret = self.collision(self.__powers[i], [2, 0])

            if(ret):
                self.__powers[i].collide()
                temp.append(self.__powers[i])

        for i in range(0, len(temp)):
            temp[i].setTime(time.time())

            ctype = temp[i].getType()

            if(ctype == 1 or ctype == 2 or ctype == 3):
                self.__paddle.release(self.__balls)

            if(ctype == 3):
                self.__ballCtr *= 2
                temp[i].power(self.__paddle, self.__balls)

    def moveBricks(self):
        for i in range(len(self.__bricks) - 1, -1, -1):
            for j in range(0, len(self.__bricks[i])):
                if(self.__bricks[i][j].getActive()):
                    for k in range(0, len(self.__powers)):
                        if(self.__powers[k].getPos() == self.__bricks[i][j].getPos() and not self.__powers[k].getActive()):
                            self.__powers[k].setVel([self.__moveBr, 0])
                            self.__powers[k].move()
                            self.__powers[k].setVel([0, 0])
                            break

                    self.__bricks[i][j].setVel([self.__moveBr, 0])
                    self.__bricks[i][j].move()
                    self.__bricks[i][j].setVel([0, 0])

                    if(self.__bricks[i][j].getPos()[0] + self.__bricks[i][j].getDim()[0] - 1 >= self.__paddle.getPos()[0]):
                        self.__lives = 1
                        self.lifeLoss()

        self.__moveBr = 0

    def lifeLoss(self):

        self.__lives -= 1

        if(not self.__lives):
            self.__score -= (time.time() - self.__start) / 10
            print(font['red'] + bg['reset'] + "You Lost! Game Over! Your final score is %.3f" %(self.__score))
            print("\033[?25h")
            quit()

        for l in range(0, len(self.__powers)):
            if(self.__powers[l].getTime() != -1):

                self.__powers[l].setTime(-1)

        self.__balls = []
        self.__balls.append(Ball([self.__paddle.getPos()[0] - 1, self.__paddle.getPos()[1] + (int)(self.__paddle.getDim()[1] / 2)]))
        self.__lifeRec = True
        self.__paddle.setStick(True)

    def won(self):
        self.__score -= (time.time() - self.__start) / 10
        if(self.__lvl == 3):
            print(font['red'] + bg['reset'] + "Congratulations! You Won! Your final score is %.3f" %(self.__score))
            print("\033[?25h")
            quit()

        else:
            print(font['red'] + bg['reset'] + "Congratulations! You cleared level %d! Your current score is %.3f" %(self.__lvl, self.__score))
            time.sleep(3)
            return True

    def timeCheck(self, tempTime, pup):
        if(pup.getTime() != -1 and tempTime - pup.getTime() - period >= 1e-3):
            pup.setTime(-1)
            ctype = pup.getType()

            if(ctype == 3):
                self.__ballCtr = (int)(np.ceil(self.__ballCtr / 2))
                pup.normal(self.__paddle, self.__balls, self.__ballCtr)

            if(ctype == 1 or ctype == 2 or ctype == 3):
                self.__paddle.release(self.__balls)

            elif(not self.__lifeRec and ctype == 6):
                self.__paddle.release(self.__balls)

    def play(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[?25l")
        ctr = 0
        # self.findPup(3).setTime(time.time())
        # self.findPup(8).setTime(time.time())

        while True:

            self.activation()

            if self.__input.kbhit():
                inp = self.__input.getch()
                retd = self.handle_input(inp)
                if(retd and self.won()):
                    return [self.__lives, self.__score]

                self.__input.flush()

            for i in range(0, len(self.__bricks)):
                for j in range(0, len(self.__bricks[i])):
                    if(ctr % brickFps == 0):
                        self.__bricks[i][j].rainbow()

            for l in range(0, len(self.__powers)):
                    oldVel = self.__powers[l].getVel()[:]

                    if(self.__powers[l].getActive() and ctr % gravFps == 0):
                        self.__powers[l].setVel([oldVel[0] + gravity, oldVel[1]])

            if(len(self.__explode)):
                self.explosion()

            self.padPowCol()

            for ball in self.__balls:
                self.collision(ball, [1, 1])

            delarr = []
            for bull in range(0, len(self.__bullets)):
                if(self.collision(self.__bullets[bull], [1, 2])):
                    delarr.append(bull)

            for bull in range(0, len(delarr)):
                del self.__bullets[delarr[bull] - bull]

            delarr = []
            loseFlag = False
            for bomb in range(0, len(self.__bombs)):
                if(self.collision(self.__bombs[bomb], [2, 0])):
                    loseFlag = True
                    delarr.append(bomb)

            for bomb in range(0, len(delarr)):
                del self.__bombs[delarr[bomb] - bomb]

            if(loseFlag):
                self.lifeLoss()

            if(self.__moveBr):
                self.moveBricks()

            if(ctr % bossFps == 0):
                self.bossMove()

            tempTime = time.time()
            for l in range(0, len(self.__powers)):
                self.timeCheck(tempTime, self.__powers[l])

                if(ctr % self.__powers[l].getFrame() == 0):
                    self.__powers[l].move()

            tmpDel = []
            below = True
            ufo = self.__bricks[0][0]
            for b in range(0, len(self.__balls)):
                if(ctr % self.__balls[b].getFrame() == 0):
                    self.__balls[b].move(1)

                if(self.__balls[b].getPos()[0] <= ufo.getPos()[0] + ufo.getDim()[0] + 2 + 3):
                    below = False

                if(not self.__balls[b].getActive()):
                    tmpDel.append(self.__balls[b])

            if(self.__spawn and below):
                self.spawnBricks(ufo)
                self.__spawn = False

            delarr = []
            for bull in range(0, len(self.__bullets)):
                if(ctr % bullFps == 0):
                    if(self.__bullets[bull].move(2)):
                        delarr.append(bull)

            for bull in range(0, len(delarr)):
                del self.__bullets[delarr[bull] - bull]

            delarr = []
            for bomb in range(0, len(self.__bombs)):
                if(ctr % bombFps == 0):
                    if(self.__bombs[bomb].move(2)):
                        delarr.append(bomb)

            for bomb in range(0, len(delarr)):
                del self.__bombs[delarr[bomb] - bomb]

            if(self.__paddle.getShoot() and ctr % bullDelay == 0):
                padPos = self.__paddle.getPos()
                padDim = self.__paddle.getDim()

                bul1 = Bullet("|", [padPos[0] - 1, padPos[1]], [-1, 0])
                bul2 = Bullet("|", [padPos[0] - 1, padPos[1] + padDim[1] - 1], [-1, 0])
                self.__bullets.append(bul1)
                self.__bullets.append(bul2)

            if(self.__lvl == lvlnum and ctr % bombDelay == 0):
                ufoPos = self.__bricks[0][0].getPos()
                ufoDim = self.__bricks[0][0].getDim()

                bom = Bullet("o", [ufoPos[0] + ufoDim[0], ufoPos[1] + (int)(ufoDim[1] / 2)], [1, 0])
                self.__bombs.append(bom)

            for ball in tmpDel:
                self.__balls.remove(ball)

            if(not self.__balls):
                self.lifeLoss()

            win = True 
            for i in range(0, len(self.__bricks)):
                for j in range(0, len(self.__bricks[i])):
                    if(self.__bricks[i][j].getType() != 1 and self.__bricks[i][j].getActive()):
                        win = False 
                        break

                if(not win):
                    break

            if(win):
                ret = self.won()
                if(ret):
                    return [self.__lives, self.__score]

            self.__screen.clear()

            print(font['white'] + bg['reset'] + "Lives: ", self.__lives)
            print(font['white'] + bg['reset'] + "Score: ", self.__score)
            print(font['white'] + bg['reset'] + "Level: ", self.__lvl)
            print(font['white'] + bg['reset'] + "Time: %.2f" %(time.time() - self.__start))

            if(self.__lvl == lvlnum):
                print(font['white'] + bg['reset'] + "Boss Life(Max 100): ", self.__bricks[0][0].getLife())

            for bull in range(0, len(self.__bullets)):
                self.__screen.populate(self.__bullets[bull])

            for i in range(0, len(self.__bricks)):
                for j in range(0, len(self.__bricks[i])):
                    self.__screen.populate(self.__bricks[i][j])

            for bomb in range(0, len(self.__bombs)):
                self.__screen.populate(self.__bombs[bomb])

            for i in range(0, len(self.__powers)):
                self.__screen.populate(self.__powers[i])

            self.__screen.populate(self.__paddle)

            for b in range(0, len(self.__balls)):
                self.__screen.populate(self.__balls[b])

            self.__screen.disp()

            time.sleep(1 / fps)
            ctr += 1
            if(ctr == 301):
                ctr = 1

            self.reset()
