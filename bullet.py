from config import *
from obj import *
from util import *

class Bullet(Object):

    def __init__(self, shap, pos, vel):

        shape = listify(shap)
        super().__init__(shape, [font['black'], bg['red']], pos, True, vel)
        self.setFrame(bullFps)
