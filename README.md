#PygameSpriteClass
The goal of this assignment is to create a functioning generic sprite class.  
When I say generic, I mean that the functionality of the class can be provided to any game entity that 
requires it either through inheritance or through inclusion of a sprite object.

#Basic (B level specifications):

 - Load graphics from graphic file(s)
 	- You may choose to either load from multiple graphic files or through sprite sheets
- Draw command
	- Specify a transparent color
- Animation commands 
	- play/pause animation
	- change animation delay
	- set animation range through a start frame and end frame
	- specify a current animation frame
	- return which animation frame the animation is currently in
	- helper functions as needed
- Rotate sprite
- Scale sprite
	- Should be able to scale up and down
- Get Width and Height (remember scaling)

#Advanced (A level specifications):

 - Fix the surface scaling problem with the Rotate command
 - Allow the user to create specific animations that are easily loaded 
 - Manipulate alpha to make sprite partially transparent
 - Debug mode that shows borders and animation frames