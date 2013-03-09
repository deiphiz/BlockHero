"""
	BLOCK HERO!
	This is a simple breakout clone, extremely modular so mess with it if you want.
	Developed by Jeremias Dulaca II <jdulaca94@gmail.com>
	No copyright whatsoever, but I do like a bit of credit if you use or modify it :)
"""


import pygame, sys, random, ConfigParser
from lib import block, ball
from pygame.locals import *
pygame.init()
pygame.mixer.init()

settings = ConfigParser.RawConfigParser()
settings.read('settings.ini')
#Window settings-----------------
FPS = settings.getint('Window', 'FPS')
WINDOWWIDTH = settings.getint('Window', 'WindowWidth')
WINDOWHEIGHT = settings.getint('Window', 'WindowHeight')
SIMPLEGRAPHICS = settings.getboolean('Window', 'SimpleGraphics')

#Player Settings-----------------
PLAYERHEIGHT = settings.getint('Player', 'PlayerHeight')
PLAYERWIDTH = settings.getint('Player', 'PlayerWidth')
PLAYERBOTTOMPOS = settings.getint('Player', 'PlayerBottomPos')
PLAYERACCEL = settings.getfloat('Player', 'PlayerAccel')
PLAYERDEACCEL = settings.getfloat('Player', 'PlayerDeAccel')
MAXPLAYERSPEED = settings.getint('Player', 'MaxPlayerSpeed')

#Ball Settings-------------------
BALLSIZE = settings.getint('Ball', 'BallSize')
BALLSPEEDY = settings.getint('Ball', 'BallSpeedY')
MAXBALLSPEEDX = settings.getint('Ball', 'MaxBallSpeedX')

#Board settings------------------
BOARDWIDTH = settings.getint('Board', 'BoardWidth')
BOARDHEIGHT = settings.getint('Board', 'BoardHeight')
BLOCKWIDTH = (WINDOWWIDTH / BOARDWIDTH) - settings.getint('Board', 'Xmargin')
BLOCKHEIGHT = (WINDOWHEIGHT / 2) / BOARDHEIGHT
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * BLOCKWIDTH))/ 2)
YMARGIN = settings.getint('Board', 'Ymargin')


#Key Bindings--------------------
LEFT = eval(settings.get('Bindings', 'MoveLeft'))
RIGHT = eval(settings.get('Bindings', 'MoveRight'))
START = eval(settings.get('Bindings', 'Start'))
RESET = eval(settings.get('Bindings', 'Reset'))
PAUSE = eval(settings.get('Bindings', 'Pause'))
MUTE = eval(settings.get('Bindings', 'Mute'))

#Jackpot-------------------------
JACKPOTCHANCE = settings.getint('Jackpot', 'JackpotChance')
assert JACKPOTCHANCE <= 100, 'You can\'t have percentage higher than 100, silly. You\'ll send the program into an infinite loop'

#color        R    G    B
WHITE	= 	(255, 255, 255)
BLACK 	= 	(  0,   0,   0)
RED 	=	(255,   0,   0)
ORANGE 	= 	(255, 165,   0)
YELLOW 	= 	(255, 255,   0)
GOLD 	= 	(255, 255,  64)
GREEN 	= 	(  0, 255,   0)
BLUE 	=	(  0,   0, 255)
DEEPBLUE=   (  0,   0,  32)
PURPLE 	= 	(255,   0, 255)

#Only needed if using simple graphics mode.
BALLCOLOR = WHITE
BACKGROUNDCOLOR = DEEPBLUE
PLAYERCOLOR = WHITE

#The alpha is used to color the blocks since the sprite is grayscale.
if SIMPLEGRAPHICS:
	BLOCKALPHA = 255
else:
	BLOCKALPHA = 128

#This tuple dictates how what colors will be assigned to each row.
COLORLIST = (RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)


paddleImage = pygame.image.load('media\\paddle.png')
paddleScaled = pygame.transform.scale(paddleImage, (PLAYERWIDTH, PLAYERHEIGHT))
ballImage = pygame.image.load('media\\ball.png')
ballScaled = pygame.transform.scale(ballImage, (BALLSIZE, BALLSIZE))
blockImage = pygame.image.load('media\\block.png')
blockScaled = pygame.transform.scale(blockImage, (BLOCKWIDTH, BLOCKHEIGHT))
bounceSound = pygame.mixer.Sound('media\\bounce.wav')
bounceSound.set_volume(0.2)
breakSound = pygame.mixer.Sound('media\\break.wav')
breakSound.set_volume(0.5)
gameWonSound = pygame.mixer.Sound('media\\gamewon.wav')
gameWonSound.set_volume(0.2)
gameOverSound = pygame.mixer.Sound('media\\gameover.wav')
gameOverSound.set_volume(0.5)

def main():
	global screen, clock, mute, gameMode
	screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), HWSURFACE, 32)
	pygame.display.set_caption('Block Hero!')
	pygame.display.set_icon(blockImage)
	clock = pygame.time.Clock()
	
	while True:
		gameMode = mainMenu()
		if gameMode == 'paddle':
			import paddlehero
			paddlehero.main()
			pygame.display.set_caption('Block Hero!')
			continue
		while True:
			result = playGame()
			if result == 'reset':
				break
			if gameOver(result) == 'reset':
				break
			
		
def playGame():
	global mute, minutes, seconds, score
	while True:
		player = pygame.Rect(int(WINDOWWIDTH / 2 - PLAYERWIDTH / 2), WINDOWHEIGHT - (PLAYERBOTTOMPOS + PLAYERHEIGHT), PLAYERWIDTH, PLAYERHEIGHT)
		playerAccel = 0
		playerSpeed = 0
		balls = [ball.Ball(player.centerx - BALLSIZE, player.top - BALLSIZE, BALLSIZE, BALLCOLOR)]
		blocks = generateNewBlocks()
		counter = 0
		seconds = 0
		minutes = 0
		score = 0
		mute = False
		
		if gameStart(player, playerAccel, playerSpeed, balls, blocks) == 'reset':
			return 'reset'
		
		while True:
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
					terminate()
				if event.type == KEYUP:
					if event.key == MUTE:
						mute = not mute
					if event.key == PAUSE:
						pause()
					if event.key == RESET:
						return 'reset'
			
			player, playerAccel, playerSpeed = movePlayer(player, playerAccel, playerSpeed)
			moveBalls(balls, player)
			score += destroyBlocks(blocks, balls)
			
			if checkWon(blocks):
				if gameMode == 'time':
					return 'won'
				if gameMode == 'survival':
					balls = [ball.Ball(player.centerx - BALLSIZE/2, player.top - BALLSIZE, BALLSIZE, BALLCOLOR)]
					balls[0].dirX, balls[0].dirY = 0, -BALLSPEEDY
					blocks = generateNewBlocks()
					if gameStart(player, playerAccel, playerSpeed, balls, blocks) == 'reset':
						return 'reset'
			
			if len(balls) == 0:
				if gameMode == 'time':
					return 'lost'
				if gameMode == 'survival':
					return score
			
			drawGame(player, blocks, balls, seconds, minutes, score)
			pygame.display.update()
			clock.tick(FPS)
			
			counter += 1
			if counter == FPS:
				counter = 0
				seconds += 1
				if seconds > 60:
					seconds = 0
					minutes += 1
					
def mainMenu():
	topSurf = font.render('Welcome to Block Hero! Choose a Game Mode.', 1, WHITE)
	topRect = topSurf.get_rect()
	topRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 - 80)

	survSurf = font.render('Survival', 1, WHITE)
	survRect = survSurf.get_rect()
	survRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
	
	timeSurf = font.render('Time Attack', 1, WHITE)
	timeRect = timeSurf.get_rect()
	timeRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 50)
	
	paddleSurf = font.render('Play Paddle Hero!', 1, YELLOW)
	paddleRect = paddleSurf.get_rect()
	paddleRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 100)
	
	options = ('survival', 'time', 'paddle')
	selectedOption = 0
	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()
			if event.type == KEYUP:
				if event.key == K_UP:
					bounceSound.play()
					selectedOption -= 1
					if selectedOption < 0:
						selectedOption = len(options) - 1
				if event.key == K_DOWN:
					bounceSound.play()
					selectedOption += 1
					if selectedOption > len(options) - 1:
						selectedOption = 0
				if event.key in (K_RETURN, K_SPACE):
					breakSound.play()
					return options[selectedOption]
		
		screen.fill(BACKGROUNDCOLOR)
		screen.blit(topSurf, topRect)
		screen.blit(survSurf, survRect)
		screen.blit(timeSurf, timeRect)
		screen.blit(paddleSurf, paddleRect)
		
		if options[selectedOption] == 'survival':
			pygame.draw.rect(screen, RED, survRect, 4)
		elif options[selectedOption] == 'time':
			pygame.draw.rect(screen, RED, timeRect, 4)
		elif options[selectedOption] == 'paddle':
			pygame.draw.rect(screen, RED, paddleRect, 4)
		
		pygame.display.update()
		clock.tick(FPS)
					
def pause():
	textobj = font.render('PAUSED', 1, WHITE, BLACK)
	textrect = textobj.get_rect()
	textrect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
	screen.blit(textobj, textrect)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()
			if event.type == KEYUP:
				if event.key == MUTE:
					mute = not mute
				if event.key == PAUSE:
					return

def generateNewBlocks():
	blocks = []
	counterX = XMARGIN
	counterY = YMARGIN
	colorCounter = 0
	for x in range(BOARDWIDTH):
		column = []
		for y in range(BOARDHEIGHT):
			column.append(block.Block(counterX, counterY, BLOCKWIDTH, BLOCKHEIGHT, COLORLIST[colorCounter], BLOCKALPHA))
			counterY += BLOCKHEIGHT
			colorCounter += 1
			if colorCounter > len(COLORLIST) -1:
				colorCounter = 0
		blocks.append(column)
		counterX += BLOCKWIDTH
		counterY = YMARGIN
		colorCounter = 0

	return blocks

def gameStart(player, playerAccel, playerSpeed, balls, blocks):
	while True:
		screen.fill(BACKGROUNDCOLOR)
		player, playerAccel, playerSpeed = movePlayer(player, playerAccel, playerSpeed)
		balls[0].centerx = player.centerx
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()
			if event.type == KEYDOWN:
				if event.key == START:
					balls[0].dirY = -BALLSPEEDY
					return
				if event.key == RESET:
					return 'reset'
				
		drawGame(player, blocks, balls, score)
		textobj = smallfont.render('Press SPACE to start', 1, WHITE)
		textrect = textobj.get_rect()
		textrect.center = (player.centerx, player.bottom + 15)
		screen.blit(textobj, textrect)	
		pygame.display.update()
		clock.tick(FPS)
	
def terminate():
	pygame.quit()
	sys.exit()
	
def movePlayer(player, playerAccel, playerSpeed):
	keys = pygame.key.get_pressed()
	playerAccel = (keys[RIGHT] - keys[LEFT]) * PLAYERACCEL

	#Player movement has acceleration. It just feels better, trust me :)
	if playerAccel != 0:
		if playerSpeed != MAXPLAYERSPEED and playerSpeed != -MAXPLAYERSPEED:
			playerSpeed += playerAccel
			if playerSpeed > MAXPLAYERSPEED:
				playerSpeed = MAXPLAYERSPEED
			if playerSpeed < -MAXPLAYERSPEED:
				playerSpeed = -MAXPLAYERSPEED

	if playerAccel == 0:
		if playerSpeed > 0:
			playerSpeed -= PLAYERDEACCEL
			if playerSpeed < 0:
				playerSpeed = 0
		if playerSpeed < 0:
			playerSpeed += PLAYERDEACCEL
			if playerSpeed > 0:
				playerSpeed = 0
				
	#In fact, if you wanna know how the game feels without acceleration, uncomment the line below.
	#playerSpeed = 10 * (keys[RIGHT] - keys[LEFT])
	player.left += playerSpeed
	if player.left < 0:
		player.left = 0
		playerSpeed = 0
	if player.right > WINDOWWIDTH:
		player.right = WINDOWWIDTH
		playerSpeed = 0
	
	return (player, playerAccel, playerSpeed)
	
def moveBalls(balls, player):
	for b in balls:
		b.left += b.dirX
		b.top += b.dirY
		
		if b.left < 0:
			b.left = 0
			if not mute:
				bounceSound.play()
			b.dirX *= -1
		if b.right > WINDOWWIDTH:
			b.right = WINDOWWIDTH
			if not mute:
				bounceSound.play()
			b.dirX *= -1
		if b.top < 0:
			b.top = 0
			if not mute:
				bounceSound.play()
			b.dirY *= -1
		if b.top > WINDOWHEIGHT:
			balls.remove(b)
		if b.colliderect(player):
			if not mute:
				bounceSound.play()
			#The further away the ball is from the center of the player,
			#The faster the ball will move on the X-Axis.
			factor = (MAXBALLSPEEDX*(b.centerx - player.centerx)) / (PLAYERWIDTH/2)
			b.bottom = player.top
			b.dirX = factor
			b.dirY *= -1
	return balls
	
def destroyBlocks(blocks, balls):
	score = 0
	for x in range(len(blocks)):
		for y in range(len(blocks[x])):
			for b in balls:
				if blocks[x][y] != None and blocks[x][y].colliderect(b):
					score += 1
					if not mute:
						breakSound.play()
					if random.randint(0, 100) <= JACKPOTCHANCE:
						score += 10
						balls.append(ball.Ball(blocks[x][y].centerx - BALLSIZE/2, blocks[x][y].top + BALLSIZE, BALLSIZE, BALLCOLOR, ( 2, BALLSPEEDY)))
						balls.append(ball.Ball(blocks[x][y].centerx - BALLSIZE/2, blocks[x][y].top + BALLSIZE, BALLSIZE, BALLCOLOR, (-2, BALLSPEEDY)))
						balls.append(ball.Ball(blocks[x][y].centerx - BALLSIZE/2, blocks[x][y].top + BALLSIZE, BALLSIZE, BALLCOLOR, ( 0, BALLSPEEDY)))
									
					#The ball hit the top right or top left corner of a block
					if (blocks[x][y].collidepoint(b.topleft) == True and\
					blocks[x][y].collidepoint(b.topright) == False) or\
					\
					(blocks[x][y].collidepoint(b.topright) == True and\
					blocks[x][y].collidepoint(b.topleft) == False):
						b.top == blocks[x][y].bottom
						if b.dirY < 0:
							b.dirY *= -1
						elif b.dirY > 0:
							b.dirX *= -1
					
					#The ball hit the top right or top left corner of a block
					elif (blocks[x][y].collidepoint(b.bottomright) == True and\
					blocks[x][y].collidepoint(b.bottomleft) == False) or\
					\
					(blocks[x][y].collidepoint(b.bottomleft) == True and\
					blocks[x][y].collidepoint(b.bottomright) == False):
						b.top == blocks[x][y].bottom
						if b.dirY > 0:
							b.dirY *= -1
						elif b.dirY < 0:
							b.dirX *= -1
					
					#The ball hit just the left side of a block
					elif blocks[x][y].collidepoint(b.topright) and\
					blocks[x][y].collidepoint(b.bottomright):
						b.right == blocks[x][y].left
						b.dirX *= -1
					
					#The ball hit just the right side of a block
					elif blocks[x][y].collidepoint(b.topleft) and\
					blocks[x][y].collidepoint(b.bottomleft):
						b.left == blocks[x][y].right
						b.dirX *= -1
					
					#The ball hit just the bottom side of a block					
					elif blocks[x][y].collidepoint(b.topleft) and\
					blocks[x][y].collidepoint(b.topright):
						b.top == blocks[x][y].bottom
						b.dirY *= -1
					
					#The ball hit just the top side of a block
					elif blocks[x][y].collidepoint(b.bottomleft) and\
					blocks[x][y].collidepoint(b.bottomright):
						b.bottom == blocks[x][y].top
						b.dirY *= -1
					
					blocks[x][y] = None
	return score

def checkWon(blocks):
	counter = 0
	for x in blocks:
		for y in x:
			if y == None:
				counter += 1
	if counter == BOARDWIDTH * BOARDHEIGHT:
		return True
	else: 
		return False

def gameOver(result):
	if not mute:
		if result == 'won':
			gameWonSound.play()
		elif result == 'lost':
			gameOverSound.play()
		else:
			gameWonSound.play()
			
	while True:
		screen.fill(BACKGROUNDCOLOR)

		if result == 'won':
			drawText('Congratulations!', font, WHITE, screen, 50, WINDOWHEIGHT/2 - 30)
			drawText('You beat the game in %s minutes and %s seconds!' %(minutes, seconds), font, WHITE, screen, 50, WINDOWHEIGHT/2)
			drawText('Press any key to start again.', font, WHITE, screen, 50, WINDOWHEIGHT/2 + 30)
			drawText('Or press "R" to return to main menu.', font, WHITE, screen, 50, WINDOWHEIGHT/2 + 60)
			
		if result == 'lost':
			drawText('You lost :(', font, WHITE, screen, 50, WINDOWHEIGHT/2 - 15)
			drawText('Press any key to start again.', font, WHITE, screen, 50, WINDOWHEIGHT/2 + 15)
			drawText('Or press "R" to return to main menu.', font, WHITE, screen, 50, WINDOWHEIGHT/2 + 45)
		
		if isinstance(result, int):
			drawText('Congratulations!', font, WHITE, screen, 50, WINDOWHEIGHT/2 - 30)
			drawText('You scored %s points!' %(result), font, WHITE, screen, 50, WINDOWHEIGHT/2)
			drawText('Press any key to start again.', font, WHITE, screen, 50, WINDOWHEIGHT/2 + 30)
			drawText('Or press "R" to return to main menu.', font, WHITE, screen, 50, WINDOWHEIGHT/2 + 60)
			
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()
			if event.type == KEYDOWN:
				if event.key == RESET:
					return 'reset'
				return
			
				
		pygame.display.update()
		clock.tick(FPS)
					
def drawGame(player, blocks, balls, seconds = 0, minutes = 0, score = 0):
	screen.fill(BACKGROUNDCOLOR)
	screen.blit(paddleScaled, player)
	for x in blocks:
		for y in x:
			if y != None:
				if not SIMPLEGRAPHICS:
					screen.blit(blockScaled, y)
				screen.blit(y.surf, y)
	for b in balls:
		if SIMPLEGRAPHICS:
			pygame.draw.rect(screen, b.color, b)
		else:
			screen.blit(ballScaled, b)
	if seconds < 10:
		padding = '0'
	else:
		padding = ''
	
	if gameMode == 'time':
		drawText('%s:%s%s' %(minutes, padding, seconds), font, WHITE, screen, 0, WINDOWHEIGHT - 30)
	if gameMode == 'survival':
		drawText('Score: %s' %(score), font, WHITE, screen, 0, WINDOWHEIGHT - 30)	
	
def drawText(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)
font = pygame.font.SysFont("Arial", 30)
smallfont = pygame.font.SysFont("Arial", 15)
	
if __name__ == '__main__':
	main()