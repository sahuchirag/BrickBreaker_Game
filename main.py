import colorama as col

from config import *
from game import *

if __name__ == "__main__":

    col.init(autoreset = False)
    cur_lives = 3
    cur_score = 0

    for lvl in range(1, lvlnum + 1):
        game = Game(cur_lives, cur_score, lvl)
        [cur_lives, cur_score] = game.play()
        del game
