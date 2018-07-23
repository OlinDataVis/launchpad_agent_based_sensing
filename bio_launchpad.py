""" Launchpad: Bio:E Focus
    Simulating the existance and usage of only one sense.
    Author: Lydia Hodges
"""
### Setup Coding Environment ###
import pygame as pg
from random import choice, randrange, uniform
from math import atan2, sqrt
from time import clock, perf_counter
import bio_sprites
from game_mech import Game

screen_width=800
screen_height=800

def conv_sec_min(time_in_sec):
    """ Convert time from seconds to minutes and seconds """
    fract_min = time_in_sec / 60
    min_to_sec = int(fract_min) * 60
    remaining_sec = time_in_sec - min_to_sec
    return (int(fract_min),int(remaining_sec))



### Initialize Main Function, Where Everything Happens ###
def main(num_o, num_prey):
    """ Main function that runs everything """
    # initialize pygame and the main display
    pg.init()
    game = Game(screen_width,screen_height)

    # initialize lists (pygame Groups) for all sprites
    all_prey = []
    prey_list = pg.sprite.Group()
    obstacle_list = pg.sprite.Group()
    all_sprites_list = pg.sprite.Group() # this is used mainly for drawing the sprites on the screen every frame

    # initialize obstacles
    for _ in range(num_o):
        obstacle = bio_sprites.Stationary(30,game.BROWN,game.BLACK,obstacle_list,all_sprites_list,screen_width,screen_height,game.rect)

    # initialize prey
    prey_movement = [-1,1]
    for _ in range(num_prey):
        prey = bio_sprites.Creature(10,15,13,prey_movement,game.BLUE,game.BLACK,prey_list,all_sprites_list,screen_width,screen_height,game.rect)
        all_prey.append(prey)



    ### Main Action, Still Within Main Function ###
    print("Start Simulation")
    game_counter = 0 # counter for every frame, used to take a picture, can be used for other things
    done = False # used to terminate the while loop
    init_time = perf_counter() # set start time so as to time the simluation
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT: # hitting the 'X' button at the top of the pygame display
                done = True

        # initialize display
        game.reset() # recolor the display so that you don't see previous frames



        ### Logic for Prey ###
        for prey in all_prey:

            # movement and avoidance
            """ These next 2 lines are unnecessary until you have multiple prey and have them interacting with each other """
            # other_list = prey_list.copy()
            # other_list.remove(prey) # use this to check if a prey is touching any other prey, not including itself
            is_touching = False
            if pg.sprite.spritecollide(prey,obstacle_list,False,pg.sprite.collide_circle): # check if prey is touching an obstacle
                is_touching = True

            if is_touching == False: # normal movement
                prey.now_move()
            else: # touching an obstacle, so backup and change velocities
                prey.rect.move_ip(prey.move[0]*-2,prey.move[1]*-2) # move_ip is a pygame function
                prey.move = (choice(prey.movement),choice(prey.movement))

            # stay in screen
            if not game.rect.contains(prey.rect):
                prey.rect.clamp_ip(game.rect) # clamp_ip is a pygame function
                prey.move = (choice(prey.movement),choice(prey.movement))
                prey.counter = 0

            """ The following logic should be uncommented when you have multiple prey and want them to interact; it is very simple logic """
            # interaction with other prey
            # if pg.sprite.spritecollide(prey,other_list,False,pg.sprite.collide_circle):
            #     other = pg.sprite.spritecollideany(prey,other_list,pg.sprite.collide_circle)
            #     prey.rect.move_ip(prey.move[0]*-2,prey.move[1]*-2)
            #     prey.move = (choice(prey.movement),choice(prey.movement))
            #
            #     other.rect.move_ip(prey.move[0]*-2,prey.move[1]*-2)
            #     other.move = (choice(prey.movement),choice(prey.movement))



        ### Update Display ###
        # show number of prey
        prey_text = pg.font.SysFont('monospace', 14)
        prey_surf = prey_text.render("Prey="+str(len(all_prey)),True,game.WHITE)
        prey_rect = prey_surf.get_rect()
        prey_rect.x = screen_width - (screen_width/10)
        prey_rect.y = screen_height/40

        # draw sprites and update the display
        all_sprites_list.draw(game.screen)
        game.screen.blit(prey_surf,prey_rect)
        pg.display.flip()

        # set max fps to 50
        game.clock.tick(50)
        game_counter += 1
        if game_counter == 1:
            pg.image.save(game.screen,"Extraneous/minimal_game.png")



    ### End Simulation ###
    # final update for end-of-simulation image
    end_time = perf_counter()
    pg.quit() # stop pygame
    elapsed_time = conv_sec_min(end_time-init_time)
    print("Simulation Complete\nScore:", elapsed_time[0], "minutes", elapsed_time[1], "seconds")



### Run Simulation from the Terminal ###
if __name__ == "__main__":
    main(15, 1)
