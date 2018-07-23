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
