""" Class File fro Bio Launchpad
    Creates: Blob class (Parent to the others), Obstacle class, Enemy class, Food class, Creature class
    Author: Lydia Hodges
"""
import pygame as pg
from random import choice, randrange
from time import clock

class Blob(pg.sprite.Sprite):
    def __init__(self, color, diameter, bgc, move=None, health=None, max_health=None):
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
        if move != None:
            self.move = move
        # handle health
        if health != None:
            self.health = health
        if max_health != None:
            self.max_health = max_health

    def conv_to_move(self,dist,i_start=-23,i_end=23,o_start=-1,o_end=1):
        in_range = i_end - i_start
        out_range = o_end - o_start
        in_x = dist[0] - i_start
        in_y = dist[1] - i_start
        out_x = ((in_x / in_range) * out_range) + o_start
        out_y = ((in_y / in_range) * out_range) + o_start
        return (out_x,out_y)

class Creature(Blob):
    def __init__(self,health,max_health,size,movement,color,bg,group,sprite_list,sc_width,sc_height,sc_rect,time=False):
        super().__init__(color,size,bg,(choice(movement),choice(movement)),health,max_health)
        # self = Blob(color,size,bg,(choice(movement),choice(movement)),health,max_health)
        self.movement = movement
        self.rect.center = (randrange(sc_width), randrange(sc_height))
        while pg.sprite.spritecollide(self,sprite_list,False,pg.sprite.collide_circle):
            self.rect.center = (randrange(sc_width), randrange(sc_height))
        self.rect.clamp_ip(sc_rect)
        self.age = 0
        group.add(self)
        sprite_list.add(self)
        if time != False:
            self.hurt = (False,None)
            self.time = clock()
        elif time == False:
            self.counter = 0
            self.hunger = False
            self.bad_pixels = []
            self.known_food = []

    def now_move(self, run=False, back=-1):
        if run == False:
            self.rect.move_ip(self.move[0],self.move[1])
        else:
            self.rect.move_ip(self.move[0]*back,self.move[1]*back)

    def bad(self):
        self.health -= 1
        self.bad_pixels.append((self.rect.center[0],self.rect.center[1]))
        self.now_move(True,-3)

    def hungery(self,loc,all_sprites,known):
        self.hunger = True
        dist = (loc[0]-self.rect.center[0],loc[1]-self.rect.center[1])
        new = self.conv_to_move(dist,-400,400,-4,4)
        if 0 < new[0]*3 < 1 or -1 < new[0]*3 < 0:
            if  0 < new[1]*3 < 1 or -1 < new[1]*3 < 0:
                known.remove(loc)
        self.move = (new[0]*3,new[1]*3)
        self.now_move()
        self.counter = 0

    def get_loc(self):
        return (self.rect.center[0] + self.move[0], self.rect.center[1] + self.move[1])

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

# def init_all(all_sprites_list,name,group,color,number,l_size,screen_width,screen_height,screen_rect,bgc,health=None,move=None,max_health=None):
#     for _ in range(number):
#         if len(l_size) > 1:
#             size = choice(l_size)
#         else:
#             size = l_size[0]
#         if move != None:
#             movement = (choice(move),choice(move))
#         else:
#             movement = None
#         name = Blob(color,size,bgc,movement,health,max_health)
#         name.rect.center = (randrange(screen_width), randrange(screen_height))
#         while pg.sprite.spritecollide(name,all_sprites_list,False,pg.sprite.collide_circle):
#             name.rect.center = (randrange(screen_width), randrange(screen_height))
#         name.rect.clamp_ip(screen_rect)
#         group.add(name)
#         all_sprites_list.add(name)
