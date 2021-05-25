import pygame, sys
from pygame.locals import *

BG = pygame.image.load('C:/Users/Thinh/cotuong_real/Img/boardchess.jpg')

class Background():
    def __init__(self):
        self.x = 0 
        self.y = 0 
        self.img = BG

    def draw(self, Screen):
        Screen.blit(self.img, (int(self.x), int(self.y)))

    def update(self):
        pass