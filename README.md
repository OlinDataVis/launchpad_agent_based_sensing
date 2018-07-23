# Agent-Based Sensory Creatures
Base page for the Agent-Based Sensory Creatures Launchpad

## Overview

This launchpad covers agent-based modeling, using sensory creatures to do so. In agent-based modeling, you have any number of 'agents', usually groups of similar things such as products or creatures, and by giving each agent it's own rules, you can observe how these agents interact with each other, with their environment (if you give them one), and anything else you provide them rules for. In this way you can model different situations and senarios and see what would come of them.

The creatures in the example have only a single sense with which to interact -- touch. You can change this as part of your extension -- either adding senses or changing the one currently used. An example of this would be giving everything 'auras' to add in smell. You can also change the number of agents (currently two, predator and prey), change the rules of the interactions, create a completely different model/simulation, or anything else that seems relevant to this launchpad. If you're not sure, feel free to ask.

![Picture of the Start of a Simulation](/Extraneous/0start_game.png)
*This is the first frame of the simulation the dev created, which the example is based on*

## Dependencies

Most of the libraries you need should have already been installed (at least if you used Anaconda to install python3). The one that might not have is pygame; to install pygame, type `pip install pygame` into your terminal. Other libraries used are as follows:

* time
* random
* math

These are just the libraries used for the example.

## Included Files

There are a couple of files that are included for the example: game_mech.py, bio_sprites.py, and bio_launchpad.py. bio_launchpad.py is the file that contains the actual simulation logic, and is the file to be run. Both game_mech.py and bio_sprites.py contain supporting code (the self-defined classes) and are imported into bio_sprites.py. Please do read through these files and understand them, and even change them if you like, but here is a quick walk through of them.

### Game_Mech

This contains the class `Game`, which is essentially the game screen. It contains the display, the clock, the various colors, and a function that is used to clean the screen every frame.

### Bio_Sprites

This file requires some knowledge of parent classes, child classes, and inheritance. If you're not too knowledgeable on this, look at the file and see if you can understand what is happening, do some research, and ask for help as needed.

This file contains the classes `Blob`, `Creature`, and `Stationary`. `Blob` is a child class of pygame's `Sprite` class, and `Creature` is a child class to `Blob`. `Stationary` is an independent class, but it does call the `Blob` class.

### Bio_Launchpad

This is the run file. There is some structure provided, since the goal of this launchpad is *not* to learn how to use pygame (feel free to explore, though!), and then you'll be walked through writing some more into this file for the example. After that, you'll be able to use it (or toss it) however you want for the extension.

## To work!

The provided code will actually run, so go ahead and do so after reading through it to see what it looks like! It should give you something like this:
![Picture of Basic Simulation](/Extraneous/minimal_game.png)

Go ahead and play around with what has been provided and see what you can do. Something a little fun to do is comment out the line that says `game.reset()`; this prevents the simulation from clearing the screen each frame, so you can get some cool effects! You can also change the number of prey and uncomment the lines that will allow multiple prey to interact with each other.

### Predators

Once you've gotten a good understanding of what's going on, try to add in some predators. You'll need to start by creating groups using `pg.sprite.Group()`, and then you'll need to create the predators using the `Creature` class, similar to the prey. You'll have to decide what size to make them and what movement to allow them, and also what color to assign them (would recommend `game.RED`). It's recommended you try running the simulation frequently to make sure everything is working, so it would be a good idea to give the predators the same logic as the prey to start and just see if they appear on the screen and move. From there, you can add more complicated movement and avoidance logic, e.g. what does a prey do when it touches a predator?

### Health and Death

Now that you have predators and prey in the same world and interacting simply with each other, it's time to get more complicated -- adding death logic. The best way to do this is to implement health logic. The `Creature` class already provides a health attribute, so now it's time to play around with it. You can change how much health the predators and prey start with, and you can include logic for gaining and losing health. Generally speaking, when a predator and prey interact in the wild, the prey 'loses health' while the predator 'gains health', and when two predators interact either  they both 'lose health' or one of them 'loses health' while the other 'gains health' (gross oversimplification, but we're trying to keep this example fairly simple). Add in some logic to both predators and prey to emulate this, or however you want them to interact (perhaps in your world the prey dominate the predators?). Once you have them losing and gaining health (restricting the number of prey to one and using a print statement for its health is a great way to test this), add in some logic for when both agents die. Do they leave behind a body? Do they simply disappear?

To kill something, you'll need to remove it from the groups it's part of (otherwise it'll still act and interact as if alive). To remove from a pygame Group, you can use `group_name.remove(sprite_name)` for each group, or to remove a sprite from all pygame Groups it is part of use `sprite_name.kill()`. Use `list_name.remove(sprite_name)` to remove from a python list (like `all_prey`). For example, writing `prey.kill()` will remove it from `prey_list` and `all_sprites_list`, meaning it won't be drawn on the screen and won't be counted towards collisions that call `prey_list`, and writing `all_prey.remove(prey)` will remove it from `all_prey` so that it won't be iterated over in the `Prey Logic` section of the main function.

You might also want to include some logic to end the simulation is all of either one or both agents is dead. For example, if you want to end the simulation when all the prey die, if you have been removing the prey from `prey_list` when they die then you can check the length of `prey_list`, and if it is length 0 have the simulation end. Can you figure out how to have the simulation end automatically? (Hint: look at the `while` loop)
