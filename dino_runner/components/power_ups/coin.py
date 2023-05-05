from dino_runner.components.power_ups.powerup import PowerUp
from dino_runner.utils.constants import COIN, COIN_TYPE


class Coin(PowerUp):
    def __init__(self):
        self.image = COIN
        self.type = COIN_TYPE
        super().__init__(self.image, self.type)