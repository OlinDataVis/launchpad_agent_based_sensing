""" Game Mechanics for Bio Launchpad """

import pygame as pg
from random import choice, randrange
import bio_sprites

class Game():
    def __init__(self,screen_width,screen_height):
        # pg.init()
        self.screen = pg.display.set_mode([screen_width, screen_height])
        self.rect = self.screen.get_rect()
        pg.display.set_caption(" Simple Agent-Based, Haptic-Only Simulation")
        self.clock = pg.time.Clock()
        self.BLACK = (0, 0, 0)# background color
        self.WHITE = (255,255,255)# text color
        self.BLUE = (0, 0, 255)# `creature` color
        self.BROWN = (139, 69, 19)# obstacle color
        self.RED = (255, 0, 0)# `enemy` color
        self.GREEN = (0, 255, 0)# `food` color

    def reset(self):
        self.screen.fill(self.BLACK)
