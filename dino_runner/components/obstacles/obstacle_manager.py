import random
import pygame
from pygame import mixer
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import BIRD, DESTROY_OBS, LARGE_CACTUS, LOSE_SOUND, SMALL_CACTUS


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.jump_sound = mixer.Sound(LOSE_SOUND)
        self.destroy = mixer.Sound(DESTROY_OBS)
    
    def update(self, game):
        if len(self.obstacles) == 0:
            aux = random.randint(0,2)
            if aux == 0:
                self.obstacles.append(Cactus(LARGE_CACTUS))
            elif aux == 1:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif aux == 2:
                self.obstacles.append(Bird(BIRD))
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.shield:
                    pygame.time.delay(1000)
                    game.playing = False
                    self.jump_sound.play()
                    game.death_count+=1
                    break
                else:
                    self.obstacles.remove(obstacle)
                    self.destroy.play()


    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def reset_obstacles(self):
        self.obstacles = []
