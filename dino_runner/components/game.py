import pygame
from pygame import mixer
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components import text_utils

from dino_runner.utils.constants import BG, BIRD, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS



class Game:
    
    ORANGE_COLOR = 'orange'
    BLACK_COLOR = 'black'


    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        #self.bird = Bird(BIRD)
        self.points = 0
        self.running = True
        self.death_count = 0
        self.coin_count = 0
        self.max_score_reached = 0

    def run(self):
        # Game loop: events - update - draw
        from dino_runner.components.power_ups.power_up_manager import PowerUpManager
        self.power_up_manager = PowerUpManager()
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.points, self.coin_count)
        self.power_up_manager.total_coins = 0
        self.game_speed = 20
        self.points = 0
        self.max_score_reached = max(self.max_score_reached, (self.coin_count*100 + self.points)) ##
        self.playing = True
        while self.playing:
            #print('max_s_r:', self.max_score_reached)
            self.events()
            self.update()
            self.draw()
            self.max_score_reached = max(self.max_score_reached, (self.coin_count*100 + self.points)) ###
        
    
    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()

    def show_menu(self):
        self.running = True
        #Print a white background
        black_color = (255, 255, 255)
        self.screen.fill(black_color)

        #Print menu elements
        self.print_menu_elements()
        pygame.display.update()
        # create a menu event handler
        self.handle_key_events_on_menu()
    
    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        

        if self.death_count == 0:
            text2, text_rect2 = text_utils.get_centered_message('DINO RUNNER GAME', self.ORANGE_COLOR, 550, 150 , 80)
            text3, text_rect3 = text_utils.get_centered_message('DINO RUNNER GAME', self.BLACK_COLOR, 545, 152 , 80)
            text, text_rect = text_utils.get_centered_message('Press any key to Start', self.BLACK_COLOR, 550, 400 )
            self.screen.blit(text3, text_rect3)
            self.screen.blit(text2, text_rect2)
            self.screen.blit(text, text_rect)
            self.screen.blit(RUNNING[0], (half_screen_width - 50, half_screen_height - 70))


        
        #######
        
        elif self.death_count > 0:   #########
            
            text2, text_rect2 = text_utils.get_centered_message('Press any Key to Restart', self.ORANGE_COLOR)
            score, score_rect = text_utils.get_centered_message('Your Score: ' + str(self.points),height=half_screen_height + 50)
            text, text_rect = text_utils.get_centered_message('Coins Collected: '+ str(self.coin_count), height=half_screen_height + 200 )
            max_score, max_score_rect = text_utils.get_centered_message('Your Score + Bonus: '+ str((self.coin_count*100) + self.points), height=half_screen_height + 100)
            death, death_rect = text_utils.get_centered_message('Death count: ' + str(self.death_count),height=half_screen_height + 250)
            max_score_per_game, mspg_rect = text_utils.get_centered_message('Max score reached: '+ str(self.max_score_reached), height=half_screen_height + 150)
                                                                
            if self.coin_count > 0: ####
                self.screen.blit(text, text_rect)
                self.screen.blit(max_score, max_score_rect)
                
            self.screen.blit(score, score_rect)
            
            self.screen.blit(max_score_per_game, mspg_rect)
            self.screen.blit(text2, text_rect2)
            self.screen.blit(death, death_rect)
            self.screen.blit(RUNNING[0], (half_screen_width - 50, half_screen_height - 130))
        

    def handle_key_events_on_menu(self):
         for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    self.coin_count = 0 ##
                    self.run()

                

                    
                    

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                
                self.running = False
        self.screen.fill((255, 255, 255))    

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player, self)
        #self.bird.update()
    

    def draw(self):
        self.score()
        self.show_coin_count() ##
        self.clock.tick(FPS)
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        text, text_rect = text_utils.get_score_element(str(self.points))
        self.player.check_invincibility(self.screen)
        self.screen.blit(text, text_rect)

    def show_coin_count(self): ####
       text2, text_rect2 = text_utils.get_coin_element(str(self.coin_count))
       self.screen.blit(text2, text_rect2)
       text, text_rect = text_utils.get_centered_message('1 COIN = +100 Points', 'black', 150, 50, 22)
       self.screen.blit(text, text_rect) 

       