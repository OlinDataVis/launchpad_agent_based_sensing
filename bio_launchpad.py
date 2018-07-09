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
    all_creatures = []
    creature_list = pg.sprite.Group()
    obstacle_list = pg.sprite.Group()
    enemy_list = pg.sprite.Group()
    food_list = pg.sprite.Group()
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

    # initialize enemies
    enemy = None
    e_movement = [-1,1]
    e_size = [25]
    bio_sprites.init_all(all_sprites_list,enemy,enemy_list,game.RED,num_e,e_size,screen_width,screen_height,game.rect,game.BLACK,25,e_movement)
    for enemy in enemy_list:
        enemy.hurt = (False,None)

    # initialize the sensor creature
    for _ in range(num_c):
        creature = bio_sprites.Creature(10,all_sprites_list,screen_width,screen_height,game.rect,game.BLUE,game.BLACK,creature_list)
        all_creatures.append(creature)
    # for _ in range(200):
    #     creature.bad_pixels.append((randrange(screen_width),randrange(screen_height)))


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

        # movement logic for enemies
        for enemy in enemy_list:
            other_list = enemy_list.copy()
            other_list.remove(enemy)
            e_is_touching = False
            if pg.sprite.spritecollide(enemy,obstacle_list,False,pg.sprite.collide_circle):
                e_is_touching = True
            if e_is_touching == False:
                enemy.rect.move_ip(enemy.move[0],enemy.move[1])
            elif e_is_touching == True:
                enemy.rect.move_ip(enemy.move[0]*-1,enemy.move[1]*-1)
                enemy.move = (choice(e_movement),choice(e_movement))
            # `friendly` logic
            if pg.sprite.spritecollide(enemy,other_list,False,pg.sprite.collide_circle):
                other = pg.sprite.spritecollideany(enemy,other_list,pg.sprite.collide_circle)
                interaction = uniform(0,1)
                if interaction <= 0.4:
                    print("'yay...'")
                    baby = bio_sprites.Blob(game.RED,25,game.BLACK,(choice(e_movement),choice(e_movement)),enemy.max_health-4)
                    baby.rect.center = (randrange(screen_width), randrange(screen_height))
                    while pg.sprite.spritecollide(baby,all_sprites_list,False,pg.sprite.collide_circle):
                        baby.rect.center = (randrange(screen_width), randrange(screen_height))
                    baby.rect.clamp_ip(game.screen_rect)
                    enemy_list.add(baby)
                    all_sprites_list.add(baby)
                    baby.hurt = (False,None)
                    enemy.health -= 2
                    other.health -= 2
                else:
                    lose = uniform(0,1)
                    if lose >= 0.5:
                        print("'Ouch...'")
                        enemy.health -= 3
                        other.health += 1
                    else:
                        print("'VICTORY!'")
                        enemy.health += 1
                        other.health -= 3
                enemy.rect.move_ip(enemy.move[0]*-2,enemy.move[1]*-2)
                enemy.move = (choice(e_movement),choice(e_movement))
            if not game.rect.contains(enemy.rect):
                enemy.rect.move_ip(enemy.move[0]*-2,enemy.move[1]*-2)
                enemy.move = (choice(e_movement),choice(e_movement))
            if enemy.hurt[0] == True and enemy.hurt[1] in creature_list:
                c = enemy.hurt[1]
                dist = ((c.rect.center[0]-enemy.rect.center[0]),(c.rect.center[1]-enemy.rect.center[1]))
                new = enemy.conv_to_move(dist)
                enemy.move = (new[0]*2,new[1]*2)
                enemy.hurt = (False,None)
            elif enemy.hurt[0] == True and enemy.hurt[1] not in creature_list:
                print("'NOMNOM'")
                if enemy.health <= enemy.max_health-1:
                    enemy.health += 2
                elif enemy.health >= enemy.max_health:
                    enemy.health += 1
                enemy.hurt = (False,None)
            # death logic
            if h_counter % 50 == 0:
                enemy.health -= 1
            if enemy.health <= 0:
                enemy.kill()

        # movement logic for creature
        for creature in all_creatures:
            other_list = creature_list.copy()
            other_list.remove(creature.body)
            c_is_touching = False
            if pg.sprite.spritecollide(creature.body,obstacle_list,False,pg.sprite.collide_circle):
                c_is_touching = True
            if c_is_touching == False and creature.counter >= 50 and creature.hunger == False:
                choose = creature.movement.copy()
                if creature.body.move[0] in choose and creature.body.move[1] in choose:
                    if creature.body.move[0] == creature.body.move[1]:
                        choose.remove(creature.body.move[0])
                    else:
                        choose.remove(creature.body.move[0])
                        choose.remove(creature.body.move[1])
                creature.body.move = (choice(choose),choice(choose))
                while creature.body.get_loc() in creature.bad_pixels:
                    # print("'Nope!'")
                    creature.body.move = (choice(choose),choice(choose))
                creature.now_move()
                creature.counter = 0
            elif c_is_touching == False and creature.counter < 50 and creature.hunger == False:
                while creature.body.get_loc() in creature.bad_pixels:
                    # print("'Nope!'")
                    creature.body.move = (choice(choose),choice(choose))
                creature.now_move()
            elif creature.hunger == True:
                while creature.body.get_loc() in creature.bad_pixels:
                    # print("'Nope!'")
                    creature.body.move = (choice(choose),choice(choose))
                creature.now_move()
            else:
                creature.now_move(True)
                creature.counter = 50
            creature.body.rect.clamp_ip(game.rect)
            # `friendly` logic
            if pg.sprite.spritecollide(creature.body,other_list,False,pg.sprite.collide_circle):
                other = pg.sprite.spritecollideany(creature.body,other_list,pg.sprite.collide_circle)
                if other.health >= 2 and creature.body.health >= 2:
                    mate_chance = uniform(0,1)
                    if mate_chance >= 0.3:
                        # print("'Yay!'")
                        baby = bio_sprites.Creature(creature.body.max_health-4,all_sprites_list,screen_width,screen_height,game.rect,game.BLUE,game.BLACK,creature_list)
                        all_creatures.append(baby)
                        other.health -= 2
                        creature.body.health -= 2
                    # else:
                        # print("'Eww...'")
                    creature.body.move = (choice(creature.movement),choice(creature.movement))
                while creature.body.get_loc() in creature.bad_pixels:
                    # print("'Nope!'")
                    creature.body.move = (choice(creature.movement),choice(creature.movement))
                creature.now_move()
                creature.counter = 0
            # eating logic
            if creature.body.health < creature.body.max_health and pg.sprite.spritecollide(creature.body,food_list,False,pg.sprite.collide_circle):
                food = pg.sprite.spritecollide(creature.body,food_list,True,pg.sprite.collide_circle)
                food = food[0]
                food.ate = True
                if food.rect.center in creature.known_food:
                    # print("'Got it'")
                    creature.known_food.remove(food.rect.center)
                if creature.body.health <= creature.body.max_health-2:
                    creature.body.health += 2
                elif creature.body.health == creature.body.max_health-1:
                    creature.body.health += 1
            elif creature.body.health >= creature.body.max_health and pg.sprite.spritecollide(creature.body,food_list,False,pg.sprite.collide_circle):
                food = pg.sprite.spritecollideany(creature.body,food_list,pg.sprite.collide_circle)
                if food.ate == False and food.rect.center not in creature.known_food:
                    creature.known_food.append(food.rect.center)
            # death logic
            if pg.sprite.spritecollide(creature.body,enemy_list,False,pg.sprite.collide_circle):
                # print("'OW!'")
                enemy = pg.sprite.spritecollideany(creature.body,enemy_list,pg.sprite.collide_circle)
                enemy.hurt = (True,(creature.body))
                if enemy.health <= enemy.max_health-1:
                    enemy.health += 1
                creature.body.health -= 1
                creature.bad()
                creature.counter = 50
            if h_counter % 50 == 0:
                creature.body.health -= 1
            if creature.body.health <= 0:
                creature.body.kill()
                all_creatures.remove(creature)
                if not all_creatures:
                    break
                # end_time = time.perf_counter()
                # all_sprites_list.draw(game.screen)
                # game.screen.blit(health_surf,health_rect)
                # pg.display.flip()
                # pg.image.save(game.screen,"0end_game.png")
                # dead = True
                # break
            # hunting logic
            elif creature.body.health <= creature.body.max_health/2 and creature.known_food:
                all_dists = []
                # print("Food List:\n", known_food)
                for location in creature.known_food:
                    dist = ((location[0]-creature.body.rect.center[0]),(location[1]-creature.body.rect.center[1]))
                    all_dists.append(dist)
                min_d = min(all_dists)
                i = all_dists.index(min_d)
                loc = creature.known_food[i]
                # if creature.body.rect.center == loc:
                #     known_food.remove(loc)
                # print("Going to:\n", loc, "From:\n", creature.body.rect.center)
                creature.hungery(loc,all_sprites_list,creature.known_food)
            else:
                creature.hunger = False

            creature.counter += 1

        # show numbers
        creature_text = pg.font.SysFont('monospace', 14)
        creature_surf = creature_text.render("Creatures="+str(len(all_creatures)),True,game.WHITE)
        creature_rect = creature_surf.get_rect()
        creature_rect.x = screen_width - (screen_width/10)
        creature_rect.y = screen_height/40

        enemy_text = pg.font.SysFont('monospace', 14)
        enemy_surf = enemy_text.render("Enemies="+str(len(enemy_list)),True,game.WHITE)
        enemy_rect = enemy_surf.get_rect()
        enemy_rect.x = screen_width/15
        enemy_rect.y = screen_height/40

        # draw sprites and update the display
        all_sprites_list.draw(game.screen)
        game.screen.blit(creature_surf,creature_rect)
        game.screen.blit(enemy_surf,enemy_rect)
        pg.display.flip()
        if not all_creatures and not enemy_list:
            break
        # set max fps to 50
        game.clock.tick(50)
        # creature.counter += 1
        h_counter += 1
        if h_counter == 1:
            pg.image.save(game.screen,"0start_game.png")
    end_time = time.perf_counter()
    pg.quit()
    # if dead == True:
    if not all_creatures:
        elapsed_time = conv_sec_min(end_time-init_time)
        print("Creatures Died\nScore:", elapsed_time[0], "minutes", elapsed_time[1], "seconds")

if __name__ == "__main__":
    main(10, 50, 10, 1000)
