import pygame

from dino_runner.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH


FONT_STYLE = 'freesansbold.ttf'
black_color = (0, 0, 0)
orange_color = 'orange'

def get_score_element(points):
    font = pygame.font.Font(FONT_STYLE, 22)

    text = font.render('Points: ' + points, True, black_color)
    text_rect = text.get_rect()
    text_rect.center = (1000, 50)
    return text, text_rect

def get_coin_element(coins): ##
    font = pygame.font.Font(FONT_STYLE, 22)

    text = font.render('Coins: ' + coins, True, orange_color)
    text_rect = text.get_rect()
    text_rect.center = (1000, 70)
    return text, text_rect


def get_centered_message (message, rcolor=black_color, width=SCREEN_WIDTH//2 , height=SCREEN_HEIGHT//2, size=30): #
    font = pygame.font.Font(FONT_STYLE, size)
    text = font.render(message, True, rcolor)
    text_rect = text.get_rect()
    text_rect.center = (width, height)
    return text, text_rect


