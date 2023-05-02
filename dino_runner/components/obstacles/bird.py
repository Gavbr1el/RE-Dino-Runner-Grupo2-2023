import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Bird(Obstacle):
    MIN_RANGE = 270    
    MAX_RANGE = 300

    def __init__(self, image):
       self.type = random.randint(0,1)
       super().__init__(image,self.type)
       if image == BIRD:
            self.rect.y = random.randint(self.MIN_RANGE, self.MAX_RANGE)