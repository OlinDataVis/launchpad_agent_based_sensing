# Agent-Based Sensory Creatures
Base page for the Agent-Based Sensory Creatures Launchpad

## Overview

<p align="center">
  <img src="/Extraneous/0start_game.png" alt="Picture of the Start of a Simulation"><br>
  <i>This is the first frame of the simulation the dev created, which the example is based on.</i>
</p>

This launchpad covers agent-based modeling, using sensory creatures to do so. In agent-based modeling, you have any number of 'agents', usually groups of similar things such as products or creatures, and by giving each agent it's own rules, you can observe how these agents interact with each other, with their environment (if you give them one), and anything else you provide them rules for. In this way you can model different situations and scenarios and see what would come of them.

In the above picture, you can see the beginning of the simulation the dev ended up making. The blue blobs are prey, the red are predators, the green are food (for the prey), and the brown are stationary obstacles. In the top left is a counter for how many predators are currently in the simulation (alive), and in the top right corner is a counter for prey. The dev's simulation including those agents and objects, predator-predator fighting and mating, prey-prey mating, predator-prey damaging, hunting, and eating, prey-food eating, food regeneration, and some slight prey memory of where food is.

The creatures in the example have only a single sense with which to interact -- touch. You can change this as part of your extension -- either adding senses or changing the one currently used. An example of this would be giving everything 'auras' to add in smell. You can also change the number of agents (currently two, predator and prey), change the rules of the interactions, create a completely different model/simulation, or anything else that seems relevant to this launchpad. If you're not sure, feel free to ask.

## Dependencies and Installs

Most of the libraries you need should have already been installed (at least if you used Anaconda to install python3). The one that might not have is pygame; to install pygame, type this into your terminal:

```
pip install pygame
```

You will be responsible for any additional libraries you use, though you can certainly ask for help.

## Resources

The dev tried to include as much of the pygame structuring as possible, but you may want to expand and add to what is being done with pygame, or you might just want to explore pygame more. Here are the resources the dev used for [sprites](https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite), [groups](https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group), [collision](https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.groupcollide) (there's lots on this page that is useful, really), [rects](https://www.pygame.org/docs/ref/rect.html) (especially the move_ip and clamp_ip functions), [display](https://www.pygame.org/docs/ref/display.html), and [surfaces](https://www.pygame.org/docs/ref/surface.html). Also, Google is definitely your friend; there are somethings that are difficult to impossible to do with pygame, but others have found some nice workarounds if you really want to do something specific.

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

<p align="center">
  <img src="/Extraneous/minimal_game.png" alt="Picture of Basic Simulation">
</p>

Go ahead and play around with what has been provided and see what you can do. Something a little fun to do is comment out the line that says `game.reset()`; this prevents the simulation from clearing the screen each frame, so you can get some cool effects! You can also change the number of prey and uncomment the lines that will allow multiple prey to interact with each other.

### Predators

Once you've gotten a good understanding of what's going on, try to add in some predators. You'll need to start by creating a group using `pg.sprite.Group()` much like `prey_list` on line 34, and then you'll need to create the predators using the `Creature` class, similar to the prey on lines 44-45. The `Group` you create is a pygame structure similar to a list; by adding sprites to it (which is done in `bio_sprites.Creature`), the `Group` will allow you to iterate through each sprite and will help keep track of collisions. If you want to see how many predators are present using `len` (e.g. in line 103 using prey), you will need to create a regular python list for the predators and add them to that as well (see lines 33 and 46 for how it was done with the prey). The full initializing code should look something like the following:

```
all_predators = []
predators_list = pg.sprites.Groups()
for _ in range(num_predators):
    predator = bio_sprites.Creature(health,size,movement,color,background_color,group_name, all_sprites_list,screen_width,screen_height,game.rect)
    all_predators.append(predator)
```

*Note: this is a block of code for visualization; this code was actually spread out in the bio_launchpad file, though you can rearrange however you wish*

When initializing the predators with the `Creature` class, you'll have to decide how much health to give them, what size to make them, what movement to allow them, and also what color to assign them (would recommend `game.RED`). `game.rect` is a call to the edges of the simulation's display screen, to keep the predator on-screen. It's recommended you try running the simulation frequently to make sure everything is working, so it would be a good idea to give the predators the same logic as the prey (lines 66-86) to start and just see if they appear on the screen and move. From there, you can add more complicated movement and avoidance logic, e.g. what does a prey do when it touches a predator?

### Health and Death

Now that you have predators and prey in the same world and interacting simply with each other, it's time to get more complicated -- adding death logic. The best way to do this is to implement health logic. The `Creature` class already provides a health attribute, so now it's time to play around with it. You can change how much health the predators and prey start with, and you can include logic for gaining and losing health. Generally speaking, when a predator and prey interact in the wild, the prey 'loses health' while the predator 'gains health', and when two predators interact either  they both 'lose health' or one of them 'loses health' while the other 'gains health' (gross oversimplification, but we're trying to keep this example fairly simple). Add in some logic to both predators and prey to emulate this, or however you want them to interact (perhaps in your world the prey dominate the predators?). Once you have them losing and gaining health (restricting the number of prey to one and using a print statement for its health is a great way to test this), add in some logic for when both agents die. Do they leave behind a body? Do they simply disappear?

To kill something, you'll need to remove it from the groups its part of (otherwise it'll still act and interact as if alive). To remove from a pygame Group, you can use `group_name.remove(sprite_name)` for each group, or to remove a sprite from all pygame Groups it is part of use `sprite_name.kill()`. Use `list_name.remove(sprite_name)` to remove from a python list (like `all_prey`). For example, writing `prey.kill()` will remove it from `prey_list` and `all_sprites_list`, meaning it won't be drawn on the screen and won't be counted towards collisions that call `prey_list`, and writing `all_prey.remove(prey)` will remove it from `all_prey` so that it won't be iterated over in the `Prey Logic` section of the main function.

You might also want to include some logic to end the simulation is all of either one or both agents is dead. For example, if you want to end the simulation when all the prey die, if you have been removing the prey from `prey_list` when they die then you can check the length of `prey_list`, and if it is length 0 have the simulation end. Can you figure out how to have the simulation end automatically? (Hint: look at the `while` loop)

### Food

Depending on what logic you have chosen to implement thus far, the prey may or may not have a way to 'gain health'. It would be good if our little blue friends stood a chance of outliving the predators, though, wouldn't it? No? At least pose more of a challenge? Whether you care for the little blue guys or not, we're adding some food for them. One of doing this is to add food as another stationary object. So, take a look at how the obstacles are initialized using the `Stationary` class (and don't forget to initialize a `food_list`), create some food,, and add some logic for it. The dev would recommend adding this logic to the prey loop rather than creating a separate loop for the food. Some things to consider: Are there different types of food (should probably start off with just one)? How much health do they give the prey? Do the prey just keep eating, or do they get full at some point? Do the predators interact with the food at all, or just ignore it?

### Remember Modeling?

Remember that this is supposed to be agent-based **_modeling_**? We have a nice simulation made, but where's the modeling? You might have noticed something popping up after each simulation that looks a bit like this:

<p align="center">
  <img src="/Extraneous/temporary.png" alt="Picture of Temporary Graph">
  <i>This is the temporary graph created by the starter code.</i>
</p>

This is a very basic graph of the elapsed time of the simulation plotted against a temporary list of ones (`temporary`) that is the same length as the time list (`plot_time`). Your goal now is to take this starter graph and create a graph showing the relationship of the populations of agents over time. This is similar to [Lotka-Volterra models](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations), which may have been mentioned in ModSim. In our case, we didn't do a simple mathematical model, we made a simulation to model the predator-prey relationship and are now graphing it so we can see it better. Below is a comparison of a Lotka-Volterra model graph and a graph created by the dev's simulation.

![Graph Comparison](/Extraneous/combined_graph.png)

Because Lotka-Volterra models are entirely equation based, they are rather predictable. In our case, we have some quite a bit of randomness, so there's little chance of predicting the outcome of each run, even if you keep the parameters the same. Also, Lotka-Volterra models have some [assumptions](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations#Physical_meaning_of_the_equations), at least some of which we actually code for and no longer have as assumptions (such as the available food for the prey). The Lotka-Volterra models and equations and definitely useful and good in some situations, so it's good to be aware of them, but keep in mind that we did not recreate the Lotka-Volterra model and so your results could look a lot different (which is also more fun).

Now, in order to actually make a graph like the ones shown above, you'll need to start keep tracking of how many predators and how many prey you have. For the sake of lining those numbers up with time you are plotting, it is recommended you add those numbers at the same time as when you log the elapsed time. In the unedited starter code, this happens in lines 121-123; since you've added code, you'll have to look for it. (Hint: Ctrl-F and plot_time are very useful here). You'll also need to change the code to get rid of the temporary list (unless you really want it) and plot the numbers of predator and prey and versus time. If you want, you can look just a little ways down [this page](https://matplotlib.org/users/pyplot_tutorial.html) to see how to plot multiple lines on one graph using just one line of code.

## Finally

That's the end of the guided example! You should have something similar to what the dev created (and you might have similar, interesting results like the one below).

<p align="center">
  <img src="/Extraneous/bio_gif.gif" alt="GIF of the End of a Simulation">
</p>

The dev also included things like loss of health over time, age and dieing of old age, regenerating food, mating between prey-prey and predator-predator, fighting between predator-predator (random, weighted chance to either fight or mate), an increase in max health each generation, predators chasing prey, and some other things. If you go back far enough in the version history of the OlinDataVis/launchpad_agent_based_sensing repo, you should be able to find the original code (all three starter files were modified) if you really want to see it.

## Extension Time!

Whether you chose to look at the dev's final code or not, that cannot be your final product. It's time for you to take agent-based modeling wherever you want it to go! You can extend the example to include more things and maybe change some of the logic, add in more creatures, or whatever you can think of, you can use the example as a rough guide for something similar, but in your own world, or you can completely scrap the example and go off on your own (though this will likely require greater knowledge and exploration of pygame). If you want a stronger bio-flavor, a recommendation would be to change what agents are present (e.g. add in something between the prey and alpha predator) and change what senses they have. As stated at the top, in the example simulation the agents are haptic only -- they only have the sense of touch in the form of collision detection. If you would like to, try to think through what he logic would be for adding one or more senses (or leaving them with only one sense and just changing what sense they have).

Whatever you choose to do, keep it reasonable to the time frame! You have other classes, other work, even other work for this class, so do enjoy yourself, but try not to over scope.

Have fun!
