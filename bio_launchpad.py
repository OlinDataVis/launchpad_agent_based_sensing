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

screen_width=1500
screen_height=1000

def conv_sec_min(time_in_sec):
    """ Convert time from seconds to minutes and seconds """
    fract_min = time_in_sec / 60
    min_to_sec = int(fract_min) * 60
    remaining_sec = time_in_sec - min_to_sec
    return (int(fract_min),int(remaining_sec))



### Initialize Main Function, Where Everything Happens ###
def main(num_prey, num_pred, num_o, num_f):
    """ Main function that runs everything """
    # initialize pygame and the main display
    pg.init()
    game = Game(screen_width,screen_height)

    # initialize lists (pygame Groups) for all sprites
    all_prey = []
    all_pred = []
    prey_list = pg.sprite.Group()
    obstacle_list = pg.sprite.Group()
    predator_list = pg.sprite.Group()
    food_list = pg.sprite.Group()
    eaten_food = pg.sprite.Group()
    all_sprites_list = pg.sprite.Group()

    # initialize obstacles
    o_size = [15, 20, 30, 40]
    for _ in range(num_o):
        size = choice(o_size)
        obstacle = bio_sprites.Stationary(size,game.BROWN,game.BLACK,obstacle_list,all_sprites_list,screen_width,screen_height,game.rect)

    # initialize food
    f_size = [5]
    for _ in range(num_f):
        food = bio_sprites.Stationary(5,game.GREEN,game.BLACK,food_list,all_sprites_list,screen_width,screen_height,game.rect,True)

    # initialize predators
    pred_movement = [-1,-2,1,2]
    e_size = [25]
    for _ in range(num_pred):
        predator = bio_sprites.Creature(25,30,25,pred_movement,game.RED,game.BLACK,predator_list,all_sprites_list,screen_width,screen_height,game.rect,True)
        all_pred.append(predator)

    # initialize prey
    prey_movement = [-1,-2,2,-1.5,1.5,-3,3,1]
    for _ in range(num_prey):
        prey = bio_sprites.Creature(10,15,13,prey_movement,game.BLUE,game.BLACK,prey_list,all_sprites_list,screen_width,screen_height,game.rect)
        all_prey.append(prey)



    ### Main Action, Still Within Main Function ###
    print("Start Simulation")
    h_counter = 0 # counter for health reduction, also used for a couple other things
    done = False # used to terminate the while loop
    init_time = perf_counter() # set start time so as to time the simluation
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT: # hitting the 'X' button at hte top of the pygame display
                done = True

        # initialize display
        game.reset() # recolor the display so that you don't see previous frames

        # reset food
        for eaten in eaten_food:
            if clock() - eaten.start >= 60:
                eaten_food.remove(eaten)
                food = bio_sprites.Stationary(5,game.GREEN,game.BLACK,food_list,all_sprites_list,screen_width,screen_height,game.rect,True)



        ### Logic for Predators ###
        # movement and avoidance
        for predator in all_pred:
            other_list = predator_list.copy()
            other_list.remove(predator)
            e_is_touching = False
            if pg.sprite.spritecollide(predator,obstacle_list,False,pg.sprite.collide_circle):
                e_is_touching = True
            if clock() - predator.time >= 2:
                predator.move = (choice(predator.movement),choice(predator.movement))
                predator.time = clock()
            if e_is_touching == False:
                predator.rect.move_ip(predator.move[0],predator.move[1])
            elif e_is_touching == True:
                predator.rect.move_ip(predator.move[0]*-1,predator.move[1]*-1)
                predator.move = (choice(predator.movement),choice(predator.movement))
                predator.time = clock()

            # interaction with other predators
            if pg.sprite.spritecollide(predator,other_list,False,pg.sprite.collide_circle):
                other = pg.sprite.spritecollideany(predator,other_list,pg.sprite.collide_circle)
                interaction = uniform(0,1)
                if interaction < 0.5 and len(all_pred)<50:
                    baby = bio_sprites.Creature(25,predator.max_health+1,25,pred_movement,game.RED,game.BLACK,predator_list,all_sprites_list,screen_width,screen_height,game.rect,True)
                    all_pred.append(baby)
                    predator.health -= 2
                    other.health -= 2
                else:
                    lose = uniform(0,1)
                    if lose >= 0.5:
                        predator.health -= 3
                        other.health += 1
                    else:
                        predator.health += 1
                        other.health -= 3
                predator.rect.move_ip(predator.move[0]*-2,predator.move[1]*-2)
                predator.move = (choice(predator.movement),choice(predator.movement))
                predator.time = clock()

            # stay in screen
            if not game.rect.contains(predator.rect):
                predator.rect.move_ip(predator.move[0]*-2,predator.move[1]*-2)
                predator.move = (choice(predator.movement),choice(predator.movement))
                predator.time = clock()

            # interaction with prey
            if predator.hurt[0] == True and predator.hurt[1] in prey_list:
                c = predator.hurt[1]
                dist = ((c.rect.center[0]-predator.rect.center[0]),(c.rect.center[1]-predator.rect.center[1]))
                new = predator.conv_to_move(dist)
                predator.move = (new[0]*3,new[1]*3)
                predator.hurt = (False,None)
                predator.time = clock()
            elif predator.hurt[0] == True and predator.hurt[1] not in prey_list:
                if predator.health <= predator.max_health-1:
                    predator.health += 2
                elif predator.health >= predator.max_health:
                    predator.health += 1
                predator.hurt = (False,None)

            # death logic
            if h_counter % 50 == 0:
                predator.health -= 1
                predator.age += 1
            if predator.age >= 30:
                predator.kill()
            if predator.health <= 0:
                predator.kill()



        ### Logic for Prey ###
        # movement and avoidance
        for prey in all_prey:
            other_list = prey_list.copy()
            other_list.remove(prey)
            c_is_touching = False
            if pg.sprite.spritecollide(prey,obstacle_list,False,pg.sprite.collide_circle):
                c_is_touching = True
            if c_is_touching == False and prey.counter >= 50 and prey.hunger == False: # change it's velocities and move
                choose = prey.movement.copy() # this chunk is to remove the current velocities to ensure the new direction will not be the same as the previous one
                if prey.move[0] in choose and prey.move[1] in choose: #
                    if prey.move[0] == prey.move[1]: #
                        choose.remove(prey.move[0]) #
                    else: #
                        choose.remove(prey.move[0]) #
                        choose.remove(prey.move[1]) #
                prey.move = (choice(choose),choice(choose))
                while prey.get_loc() in prey.bad_pixels: # avoid places where it has been attacked by a predator before
                    prey.move = (choice(choose),choice(choose))
                prey.now_move()
                prey.counter = 0
            elif c_is_touching == False and prey.counter < 50 and prey.hunger == False: # normal movement
                while prey.get_loc() in prey.bad_pixels: # avoid places where it has been attacked by a predator before
                    prey.move = (choice(choose),choice(choose))
                prey.now_move()
            elif prey.hunger == True: # health is low, go to where it knows it has touched food but didn't eat it previously
                while prey.get_loc() in prey.bad_pixels: # avoid places where it has been attacked by a predator before
                    prey.move = (choice(choose),choice(choose))
                prey.now_move()
            else: # touching a predator, so move back and change velocities
                prey.now_move(True)
                prey.counter = 50

            # stay in screen
            if not game.rect.contains(prey.rect):
                prey.rect.move_ip(prey.move[0]*-2,prey.move[1]*-2)
                prey.move = (choice(prey.movement),choice(prey.movement))
                prey.counter = 0

            # interaction with other prey
            if pg.sprite.spritecollide(prey,other_list,False,pg.sprite.collide_circle):
                other = pg.sprite.spritecollideany(prey,other_list,pg.sprite.collide_circle)
                if other.health >= 2 and prey.health >= 2:
                    mate_chance = uniform(0,1)
                    if mate_chance >= 0.4 and len(all_prey)<50:
                        baby = bio_sprites.Creature(10,prey.max_health+1,13,prey_movement,game.BLUE,game.BLACK,prey_list,all_sprites_list,screen_width,screen_height,game.rect)
                        all_prey.append(baby)
                        other.health -= 2
                        prey.health -= 2
                    prey.move = (choice(prey.movement),choice(prey.movement))
                while prey.get_loc() in prey.bad_pixels:
                    prey.move = (choice(prey.movement),choice(prey.movement))
                prey.now_move()
                prey.counter = 0

            # interaction with food
            if prey.health < prey.max_health and pg.sprite.spritecollide(prey,food_list,False,pg.sprite.collide_circle):
                food = pg.sprite.spritecollideany(prey,food_list,pg.sprite.collide_circle)
                eaten_food.add(food)
                food_list.remove(food)
                all_sprites_list.remove(food)
                food.ate = True
                food.start = clock()
                if food.rect.center in prey.known_food:
                    prey.known_food.remove(food.rect.center)
                if prey.health <= prey.max_health-2:
                    prey.health += 2
                elif prey.health == prey.max_health-1:
                    prey.health += 1
            elif prey.health >= prey.max_health and pg.sprite.spritecollide(prey,food_list,False,pg.sprite.collide_circle):
                food = pg.sprite.spritecollideany(prey,food_list,pg.sprite.collide_circle)
                if food.ate == False and food.rect.center not in prey.known_food:
                    prey.known_food.append(food.rect.center)

            # death logic
            if pg.sprite.spritecollide(prey,predator_list,False,pg.sprite.collide_circle):
                predator = pg.sprite.spritecollideany(prey,predator_list,pg.sprite.collide_circle)
                predator.hurt = (True,(prey))
                if predator.health <= predator.max_health-2:
                    predator.health += 2
                elif predator.health <= predator.max_health-1:
                    predator.health += 1
                prey.health -= 2
                prey.bad()
                prey.counter = 50
            if h_counter % 50 == 0:
                prey.health -= 1
                prey.age += 1
            if prey.age >= 30:
                prey.kill()
                all_prey.remove(prey)
                continue
            if prey.health <= 0:
                prey.kill()
                all_prey.remove(prey)
                continue

            # hunting logic, continuing from if statement above
            elif prey.health <= prey.max_health/2 and prey.known_food:
                all_dists = []
                for location in prey.known_food:
                    dist = ((location[0]-prey.rect.center[0]),(location[1]-prey.rect.center[1]))
                    all_dists.append(dist)
                min_d = min(all_dists)
                i = all_dists.index(min_d)
                loc = prey.known_food[i]
                prey.hungery(loc,all_sprites_list,prey.known_food)
            else:
                prey.hunger = False

            prey.counter += 1



        ### Update Display ###
        # show number of predators and prey
        prey_text = pg.font.SysFont('monospace', 14)
        prey_surf = prey_text.render("Prey="+str(len(all_prey)),True,game.WHITE)
        prey_rect = prey_surf.get_rect()
        prey_rect.x = screen_width - (screen_width/10)
        prey_rect.y = screen_height/40

        predator_text = pg.font.SysFont('monospace', 14)
        predator_surf = predator_text.render("Predators="+str(len(predator_list)),True,game.WHITE)
        predator_rect = predator_surf.get_rect()
        predator_rect.x = screen_width/15
        predator_rect.y = screen_height/40

        # draw sprites and update the display
        all_sprites_list.draw(game.screen)
        game.screen.blit(prey_surf,prey_rect)
        game.screen.blit(predator_surf,predator_rect)
        pg.display.flip()
        if not all_prey and not predator_list: # if all predators and prey are dead, exit the simulation
            done = True

        # set max fps to 50
        game.clock.tick(50)
        h_counter += 1
        if h_counter == 1:
            pg.image.save(game.screen,"Extraneous/0start_game.png")



    ### End Simulation ###
    # final update for end-of-simulation image
    end_time = perf_counter()
    all_sprites_list.draw(game.screen)
    game.screen.blit(prey_surf,prey_rect)
    game.screen.blit(predator_surf,predator_rect)
    pg.display.flip()
    pg.image.save(game.screen,"Extraneous/0end_game.png")
    pg.quit() # stop pygame
    if not all_prey or not predator_list: # if either all predators or prey are dead, consider the simulation complete and get the time
        elapsed_time = conv_sec_min(end_time-init_time)
        print("Simulation Complete\nScore:", elapsed_time[0], "minutes", elapsed_time[1], "seconds")



### Run Simulation from the Terminal ###
if __name__ == "__main__":
    main(15, 13, 50, 1000)
