# GUI-based Game: #SGUNITED
#SGUNITED by Marcus Ho Jun Wei, Student ID: 1004271

## Table of contents
* [Inspiration](#inspiration)
* [Summary](#summary)
* [How to play](#how-to-play)
* [Technologies](#technologies)
* [Concepts used](#concepts-used)
* [Design and thought process](#Design-and-thought-process)
* [Contact](#contact)

## Inspiration
In view of the current pandemic, I was inspired to create a game that would not only be fun for the user, but also raise awareness to users of all ages with regards to how to best survive this difficult period. As the game Flappy Bird gained huge success back in 2013, I wanted to create a similar game as I believe it would be most effective in spreading the educational message, especially to younger children.

## Summary
#SGUNITED is a GUI-based game that is easy to play and yet, very addictive. It only involves the use of mouseclicks and nothing more!

## How to play 
1. A text "Start your survival!" will be appear on the centre of your window.
2. Click anywhere to start the game!
3. After the first click, any subsequent clicks will make your character jump up vertically while not clicking will make your character accelerate downwards vertically.
4. As the COVID19 virus blocks approach you, your goal is to avoid contact with the blocks by maintaining your vertical position between the gap of the blocks.
5. Everytime you successfully hover through the gap of the blocks, you will gain one point as seen at the bottom of your window.
6. If your character comes in contact with the mask (which is randomly spawned in the game), you will gain an extra 10 points to your current score.
7. However, if your character collides with the virus blocks, the ground or the ceiling, the game is over and your final will be recorded at the bottom of your window
8. You may then click on anywhere on the screen to try again!

## Technologies
* Kivy
* Python 3
* Kivy Language
* VScode (IDE)

## Concepts used
* Object Oriented Programming
* Creating a Widget tree in .kv file
* Binding of widgets to callbacks
* Manipulating widgets
* Using canvas to draw on screen

## Design and thought process
At first, I did not intend to use kivy language to code my game. However, after reading up extensively online, I realized that kivy language allows you to create your widget tree in a declarative way and also, to bind widgets to callbacks in a natural manner. Hence, I was able to use Python to showcase the logic of my game while use kvlang to work on the interface of my game. This allowed me to code faster and more efficiently compared to if I only used Python to code my game.

In my game, I have chosen the FloatLayout as my root widget because my widgets would be unrestricted and it's the most flexible layout compared to the others available. 
The main child widgets I created under the root widget are:
1. Background
2. Pipe
3. Button
4. Merlion
5. Mask
6. Label(Score)

Background: This child widget mainly consists of 3 rectangles drawn using canvas. The 1st rectangle represents the background colour of the game which is just an image. The 2nd and 3rd rectangle contains textures of the SGUNITE logo and the floor respectively. The textures are used to allow the pictures to repeat. This is done through scrolling of the textures by updating its uvpos attribute followed by telling the textures parent widget to redraw it.

Pipe: I created 5 child widgets which refer to the Pipe class I created in the Python file. The pipe child widgets refers to the COVID19 virus blocks in my game. In each child widget, I defined the size, position and id of the widget. Each pipe widget also uses canvas to draw two rectangles, the bottom pipe and the top pipe. In my Pipe class, I assigned the value of the gap size between the bottom and top pipe and this value is constant throughout of all pipes. I varied the height of the bottom pipe by importing the random module and this results in the variance of bottom pipe height for the 5 pipes.

Button: This child widget refers to the button which appears when the game is run. With a transparent background that fills up the entire screen, after the button is pressed and released, the game commences and the button is disabled. The button is then re-enabled when the game is over.

Merlion: This child widget refers to the merlion character which will be used to avoid the virus blocks. Using the physics logic from flappy bird, I binded the widget with the on_touch_down event which would define the vertical velocity of the widget.

Mask: This child widget refers to the mask which appears at a specific interval in the game.

Label: This child widget refers to the score at the bottom of the screen which keeps track of the user's progress.

To enable movement of the Pipe and Mask widget across the screen, I imported the kivy clock module which allowed me to take the time passed as an argument. With Clock.schedule_interval(), it allows me to callback a particular function every x seconds I choose. With the time passed as an argument, I deducted it from the x-coordinate position of my Pipe and Mask widget and hence this results in a new position of the widgets on my screen.

As detection of collision between widgets is essential for my game, I used __.collide_widget() and if else statements to code the results I wanted when collisions did and did not occur.

## Contact
Created by Marcus Ho Jun Wei, Cohort Class 5