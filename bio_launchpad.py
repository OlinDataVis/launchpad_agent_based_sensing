""" Launchpad: Bio:E Focus
    Simulating the existance and usage of only one sense.
    Author: Lydia Hodges
"""

import pygame as pg
from random import choice, randrange, uniform
from math import atan2, sqrt
import time
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

# def conv_to_move(dist,i_start=-23,i_end=23,o_start=-1,o_end=1):
#     in_range = i_end - i_start
#     out_range = o_end - o_start
#     in_x = dist[0] - i_start
#     in_y = dist[1] - i_start
#     out_x = ((in_x / in_range) * out_range) + o_start
#     out_y = ((in_y / in_range) * out_range) + o_start
#     return (out_x,out_y)

def main(num_c, num_o, num_e, num_f):
    """ Main function that runs everything """
    pg.init()
    game = Game(screen_width,screen_height)

    # initialize lists (pygame Groups) for all sprites
    all_prey = []
    prey_list = pg.sprite.Group()
    obstacle_list = pg.sprite.Group()
    predator_list = pg.sprite.Group()
    food_list = pg.sprite.Group()
    eaten_food = pg.sprite.Group()
    all_sprites_list = pg.sprite.Group()

    # initialize obstacles
    obstacle = None
    o_size = [15, 20, 30, 40]
    bio_sprites.init_all(all_sprites_list,obstacle,obstacle_list,game.BROWN,num_o,o_size,screen_width,screen_height,game.rect,game.BLACK)

    # initialize food
    food = None
    f_size = [5]
    bio_sprites.init_all(all_sprites_list,food,food_list,game.GREEN,num_f,f_size,screen_width,screen_height,game.rect,game.BLACK)
    for food in food_list:
        food.ate = False

    # initialize predators
    predator = None
    e_movement = [-1,-2,1,2]
    e_size = [25]
    bio_sprites.init_all(all_sprites_list,predator,predator_list,game.RED,num_e,e_size,screen_width,screen_height,game.rect,game.BLACK,25,e_movement,30)
    for predator in predator_list:
        predator.hurt = (False,None)
        predator.age = 0
        predator.counter = time.clock()

    # initialize prey
    for _ in range(num_c):
        prey = bio_sprites.Creature(10,15,all_sprites_list,screen_width,screen_height,game.rect,game.BLUE,game.BLACK,prey_list)
        all_prey.append(prey)


    ### Main Action ###
    print("Start Simulation")
    h_counter = 0
    dead = False
    done = False
    init_time = time.perf_counter()
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        # initialize display
        game.reset()

        # reset food
        for eaten in eaten_food:
            if time.clock() - eaten.start >= 60:
                eaten_food.remove(eaten)
                # food_list.add(eaten)
                # all_sprites_list.add(eaten)
                food = bio_sprites.Blob(game.GREEN,5,game.BLACK)
                food.rect.center = (randrange(screen_width), randrange(screen_height))
                while pg.sprite.spritecollide(food,all_sprites_list,False,pg.sprite.collide_circle):
                    food.rect.center = (randrange(screen_width), randrange(screen_height))
                food.rect.clamp_ip(game.screen_rect)
                food.ate = False
                food_list.add(food)
                all_sprites_list.add(food)

        # movement logic for predators
        for predator in predator_list:
            other_list = predator_list.copy()
            other_list.remove(predator)
            e_is_touching = False
            if pg.sprite.spritecollide(predator,obstacle_list,False,pg.sprite.collide_circle):
                e_is_touching = True
            if time.clock() - predator.counter >= 2:
                predator.move = (choice(e_movement),choice(e_movement))
                predator.counter = time.clock()
            if e_is_touching == False:
                predator.rect.move_ip(predator.move[0],predator.move[1])
            elif e_is_touching == True:
                predator.rect.move_ip(predator.move[0]*-1,predator.move[1]*-1)
                predator.move = (choice(e_movement),choice(e_movement))
                predator.counter = time.clock()
            # `friendly` logic
            if pg.sprite.spritecollide(predator,other_list,False,pg.sprite.collide_circle):
                other = pg.sprite.spritecollideany(predator,other_list,pg.sprite.collide_circle)
                interaction = uniform(0,1)
                if interaction < 0.5:
                    # print("'Yay...'")
                    baby = bio_sprites.Blob(game.RED,25,game.BLACK,(choice(e_movement),choice(e_movement)),15,predator.max_health+1)
                    baby.rect.center = (randrange(screen_width), randrange(screen_height))
                    while pg.sprite.spritecollide(baby,all_sprites_list,False,pg.sprite.collide_circle):
                        baby.rect.center = (randrange(screen_width), randrange(screen_height))
                    baby.rect.clamp_ip(game.screen_rect)
                    predator_list.add(baby)
                    all_sprites_list.add(baby)
                    baby.hurt = (False,None)
                    baby.counter = time.clock()
                    baby.age = 0
                    predator.health -= 2
                    other.health -= 2
                else:
                    lose = uniform(0,1)
                    if lose >= 0.5:
                        # print("'Ouch...'")
                        predator.health -= 3
                        other.health += 1
                    else:
                        # print("'VICTORY!'")
                        predator.health += 1
                        other.health -= 3
                predator.rect.move_ip(predator.move[0]*-2,predator.move[1]*-2)
                predator.move = (choice(e_movement),choice(e_movement))
                predator.counter = time.clock()
            # stay in screen
            if not game.rect.contains(predator.rect):
                predator.rect.move_ip(predator.move[0]*-2,predator.move[1]*-2)
                predator.move = (choice(e_movement),choice(e_movement))
                predator.counter = time.clock()
            # eating logic
            if predator.hurt[0] == True and predator.hurt[1] in prey_list:
                c = predator.hurt[1]
                dist = ((c.rect.center[0]-predator.rect.center[0]),(c.rect.center[1]-predator.rect.center[1]))
                new = predator.conv_to_move(dist)
                predator.move = (new[0]*3,new[1]*3)
                predator.hurt = (False,None)
                predator.counter = time.clock()
            elif predator.hurt[0] == True and predator.hurt[1] not in prey_list:
                # print("'NOMNOM'")
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

        # movement logic for prey
        for prey in all_prey:
            other_list = prey_list.copy()
            other_list.remove(prey.body)
            c_is_touching = False
            if pg.sprite.spritecollide(prey.body,obstacle_list,False,pg.sprite.collide_circle):
                c_is_touching = True
            if c_is_touching == False and prey.counter >= 50 and prey.hunger == False:
                choose = prey.movement.copy()
                if prey.body.move[0] in choose and prey.body.move[1] in choose:
                    if prey.body.move[0] == prey.body.move[1]:
                        choose.remove(prey.body.move[0])
                    else:
                        choose.remove(prey.body.move[0])
                        choose.remove(prey.body.move[1])
                prey.body.move = (choice(choose),choice(choose))
                while prey.body.get_loc() in prey.bad_pixels:
                    # print("'Nope!'")
                    prey.body.move = (choice(choose),choice(choose))
                prey.now_move()
                prey.counter = 0
            elif c_is_touching == False and prey.counter < 50 and prey.hunger == False:
                while prey.body.get_loc() in prey.bad_pixels:
                    # print("'Nope!'")
                    prey.body.move = (choice(choose),choice(choose))
                prey.now_move()
            elif prey.hunger == True:
                while prey.body.get_loc() in prey.bad_pixels:
                    # print("'Nope!'")
                    prey.body.move = (choice(choose),choice(choose))
                prey.now_move()
            else:
                prey.now_move(True)
                prey.counter = 50
            prey.body.rect.clamp_ip(game.rect)
            # `friendly` logic
            if pg.sprite.spritecollide(prey.body,other_list,False,pg.sprite.collide_circle):
                other = pg.sprite.spritecollideany(prey.body,other_list,pg.sprite.collide_circle)
                if other.health >= 2 and prey.body.health >= 2:
                    mate_chance = uniform(0,1)
                    if mate_chance >= 0.4 and len(all_prey)<=100:
                        # print("'Yay!'")
                        baby = bio_sprites.Creature(5,prey.body.max_health+1,all_sprites_list,screen_width,screen_height,game.rect,game.BLUE,game.BLACK,prey_list)
                        all_prey.append(baby)
                        other.health -= 2
                        prey.body.health -= 2
                    # else:
                        # print("'Eww...'")
                    prey.body.move = (choice(prey.movement),choice(prey.movement))
                while prey.body.get_loc() in prey.bad_pixels:
                    # print("'Nope!'")
                    prey.body.move = (choice(prey.movement),choice(prey.movement))
                prey.now_move()
                prey.counter = 0
            # eating logic
            if prey.body.health < prey.body.max_health and pg.sprite.spritecollide(prey.body,food_list,False,pg.sprite.collide_circle):
                food = pg.sprite.spritecollideany(prey.body,food_list,pg.sprite.collide_circle)
                # food = food[0]
                eaten_food.add(food)
                food_list.remove(food)
                all_sprites_list.remove(food)
                food.ate = True
                food.start = time.clock()
                if food.rect.center in prey.known_food:
                    # print("'Got it'")
                    prey.known_food.remove(food.rect.center)
                if prey.body.health <= prey.body.max_health-2:
                    prey.body.health += 2
                elif prey.body.health == prey.body.max_health-1:
                    prey.body.health += 1
            elif prey.body.health >= prey.body.max_health and pg.sprite.spritecollide(prey.body,food_list,False,pg.sprite.collide_circle):
                food = pg.sprite.spritecollideany(prey.body,food_list,pg.sprite.collide_circle)
                if food.ate == False and food.rect.center not in prey.known_food:
                    prey.known_food.append(food.rect.center)
            # death logic
            if pg.sprite.spritecollide(prey.body,predator_list,False,pg.sprite.collide_circle):
                # print("'OW!'")
                predator = pg.sprite.spritecollideany(prey.body,predator_list,pg.sprite.collide_circle)
                predator.hurt = (True,(prey.body))
                if predator.health <= predator.max_health-2:
                    predator.health += 2
                elif predator.health <= predator.max_health-1:
                    predator.health += 1
                prey.body.health -= 2
                prey.bad()
                prey.counter = 50
            if h_counter % 50 == 0:
                prey.body.health -= 1
                prey.age += 1
            if prey.age >= 30:
                prey.body.kill()
                all_prey.remove(prey)
                continue
            if prey.body.health <= 0:
                prey.body.kill()
                all_prey.remove(prey)
                continue
            # hunting logic
            elif prey.body.health <= prey.body.max_health/2 and prey.known_food:
                all_dists = []
                # print("Food List:\n", known_food)
                for location in prey.known_food:
                    dist = ((location[0]-prey.body.rect.center[0]),(location[1]-prey.body.rect.center[1]))
                    all_dists.append(dist)
                min_d = min(all_dists)
                i = all_dists.index(min_d)
                loc = prey.known_food[i]
                # if prey.body.rect.center == loc:
                #     known_food.remove(loc)
                # print("Going to:\n", loc, "From:\n", prey.body.rect.center)
                prey.hungery(loc,all_sprites_list,prey.known_food)
            else:
                prey.hunger = False

            prey.counter += 1

        # show numbers
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
        if not all_prey and not predator_list:
            break
        # set max fps to 50
        game.clock.tick(50)
        # prey.counter += 1
        h_counter += 1
        if h_counter == 1:
            pg.image.save(game.screen,"Extraneous/0start_game.png")
    end_time = time.perf_counter()
    all_sprites_list.draw(game.screen)
    game.screen.blit(prey_surf,prey_rect)
    game.screen.blit(predator_surf,predator_rect)
    pg.display.flip()
    pg.image.save(game.screen,"Extraneous/0end_game.png")
    pg.quit()
    # if dead == True:
    if not all_prey or not predator_list:
        elapsed_time = conv_sec_min(end_time-init_time)
        print("Simulation Complete\nScore:", elapsed_time[0], "minutes", elapsed_time[1], "seconds")

if __name__ == "__main__":
    main(15, 50, 13, 1000)
