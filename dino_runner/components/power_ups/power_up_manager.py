import random
import pygame
from dino_runner.components.power_ups.coin import Coin
from dino_runner.components.power_ups.shield import Shield
from dino_runner.utils.constants import COIN_SOUND, SHIELD_SOUND
from pygame import mixer

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appers = 0
        self.points = 0
        self.shield_sound = mixer.Sound(SHIELD_SOUND)
        self.coin_sound = mixer.Sound(COIN_SOUND)
    
    def update(self, points, game_speed, player, game):
        self.generate_power_ups(points)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if power_up.type == "shield": #####
                if player.dino_rect.colliderect(power_up.rect):
                    power_up.start_time = pygame.time.get_ticks()
                    player.shield = True
                    player.show_text = True
                    player.type = power_up.type
                    time_random = random.randrange(5, 8)
                    player.shield_time_up = power_up.start_time + (time_random * 1000)
                    self.power_ups.remove(power_up)
                    self.shield_sound.play()
            elif player.dino_rect.colliderect(power_up.rect): 
                self.power_ups.remove(power_up)
                game.coin_count +=1
                self.coin_sound.play()
    

                

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
    
    def reset_power_ups(self, points, coin_count):
        self.power_ups = []
        self.points = points
        self.coin_count = coin_count
        self.when_appers = self.points + random.randint(50, 100)


    def generate_power_ups(self, points):
        self.points = points
        if len(self.power_ups) == 0:
            if self.when_appers == self.points:
                aux = random.randint(0, 1)
                if aux == 0:
                    print ("generating powerups")
                    self.power_ups.append(Shield())
                    self.when_appers = random.randint(self.when_appers+200, self.when_appers+400)
                else:
                    print ("generating powerups")
                    self.power_ups.append(Coin())
                    self.when_appers = random.randint(self.when_appers+100, self.when_appers+200)
        return self.power_ups