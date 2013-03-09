##~~~~~~~~~~~~~~~~~~~~~##
#  THIS IS BLOCK HERO!  #
##~~~~~~~~~~~~~~~~~~~~~##
~ver 1.1

Block Hero! is a simple breakout clone.
- Move left and right using the arrow keys. 
- Press "M" to mute the sound.
- Press "P" to pause the game
- Press "R" anytime to return to the main menu
- For every block you hit, there is a 5% chance to get 3 more blocks!

In Time Attack mode, you try to clear the board as fast as you can!
In Survival mode, the game goes forever, resetting the board every time you clear it. Try to get the highest score!

You can also change how the game is played by modifying the "settings.ini" file.

Developed by Jeremias Dulaca II. Email any questions to him at <jdulaca94@gmail.com>.

##~~~~~~~~~~~~~~~~~~~~~##
#   NEW: PADDLE HERO!   #
##~~~~~~~~~~~~~~~~~~~~~##

Paddle Hero! is a simple Pong clone.
- Player 1 is on the right, Player 2 is on the left
- Control Player 1 with the UP and DOWN arrow keys
- Control Player 2 with the "W" and "S" keys
- Press "M" to mute the sound.
- Press "P" to pause the game
- Press "R" anytime to return to the main menu

Paddle Hero shares the same settings with Block Hero, though you can't change most of the items.

Developed by Jeremias Dulaca II. Email any questions to him at <jdulaca94@gmail.com>.


##~~~~~~~~~~~##
#  CHANGELOG  #
##~~~~~~~~~~~##

ver 1.1:

* Changed almost all graphics and sound. Playing the game will be MUCH easier on the eyes and ears:
	- Block sprite changed.
	- Ball sprite cleaned up a bit.
	- The paddle now has a sprite.
	- Every sound is changed except for the game won sound.
	- Background is now a dark blue instead of black.

* Changed layout of blocks and size of ball. You can now control how much space is on either side of the board with the "Xmargin" option in the settings.ini

* Added a new game mode:
	- The original game mode is now called "Time Attack"
	- The new game mode, "Survival" is akin to the original Atari 2600 Breakout, where blocks get refreshed indefinitely until you lose your balls.

* Integrated "Paddle Hero!", a simple pong clone built of the code of Block Hero, into the main game:
	- Access the new game from the main menu
	- You may return to Block Hero! anytime through Paddle Hero!'s main menu


ver 1.02:

* Added Paddle Hero to the package

* Other small, insignificant changes to the code


ver 1.01:

* Cleaned up code a bit after learning about OOP. Means nothing to the end user since performance is still the same, but you'll notice the new "lib" folder in the source with all my classes.

* Changed default game settings slightly to make it more challenging.

* Added a "Ymargin" setting to settings.ini. Change it to shift the game board down by board values. It makes it look more like the Atari 2600 Breakout.