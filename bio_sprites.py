""" Class File fro Bio Launchpad
    Creates: Blob class (Parent to the others), Obstacle class, Enemy class, Food class, Creature class
    Author: Lydia Hodges
"""
import pygame as pg
from random import choice, randrange
from time import clock

class Blob(pg.sprite.Sprite):
    def __init__(self, color, diameter, bgc):
        """ Initialize all objects/beings as circular `blobs` of specified
            color and size. Default values are for `obstacles`.
        """
        # initialize the Sprite parent class
        super().__init__()

        # create the image for the blob, then set it's background to transparent
        self.image = pg.Surface([diameter,diameter])
        self.image.fill(bgc)
        self.image.set_colorkey(bgc) # this is a pygame function to set all pixels that are the given color to transparent

        # draw the ellipsoidal shape of the blob
        pg.draw.ellipse(self.image, color, [0,0,diameter,diameter])

        # get the rectangle that surrounds the sprite -- this is used to set/move location
        self.rect = self.image.get_rect()
        # set the radius for the sprite -- this will be used for circle collision
        self.radius = diameter/2

class Creature(Blob):
    def __init__(self,health,size,movement,color,bg,group,sprite_list,sc_width,sc_height,sc_rect,time=False):
        super().__init__(color,size,bg)
        self.move = (choice(movement),choice(movement))
        self.health = health
        self.movement = movement
        self.rect.center = (randrange(sc_width), randrange(sc_height))
        while pg.sprite.spritecollide(self,sprite_list,False,pg.sprite.collide_circle):
            self.rect.center = (randrange(sc_width), randrange(sc_height))
        self.rect.clamp_ip(sc_rect)
        self.age = 0
        group.add(self)
        sprite_list.add(self)

    def now_move(self, run=False, back=-1):
        if run == False:
            self.rect.move_ip(self.move[0],self.move[1])
        else:
            self.rect.move_ip(self.move[0]*back,self.move[1]*back)

class Stationary():
    def __init__(self,size,color,bg,group,all_sprites,sc_width,sc_height,sc_rect,decay=False):
        self = Blob(color,size,bg)
        self.rect.center = (randrange(sc_width),randrange(sc_height))
        while pg.sprite.spritecollide(self,all_sprites,False,pg.sprite.collide_circle):
            self.rect.center = (randrange(sc_width),randrange(sc_height))
        self.rect.clamp_ip(sc_rect)
        if decay != False:
            self.ate = False
        group.add(self)
        all_sprites.add(self)
