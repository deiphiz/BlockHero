import pygame, sys, random, ConfigParser
from pygame.locals import *
from lib.ball import Ball
from lib.player import Player

pygame.init()

settings = ConfigParser.RawConfigParser()
settings.read('settings.ini')
FPS = settings.getint('Window', 'FPS')
WINDOWWIDTH = settings.getint('Window', 'WindowWidth')
WINDOWHEIGHT = settings.getint('Window', 'WindowHeight')

SCORELIMIT = 5

PLAYERHEIGHT = settings.getint('Player', 'PlayerWidth')
PLAYERWIDTH = settings.getint('Player', 'PlayerHeight')
PLAYERPOS = 30
PLAYERACCEL = 0.7
PLAYERDEACCEL = 0.7
MAXPLAYERSPEED = 20

AISTUPIDITY = 5
AIACCEL = 1.0
AIDEACCEL = 0.5
MAXAISPEED = 20

BALLSIZE = 20
BALLSPEEDX = 10
MAXBALLSPEEDY = 12

P1UP = K_UP
P1DOWN = K_DOWN
P2UP = K_w
P2DOWN = K_s
START = K_SPACE
PAUSE = K_p
MUTE = K_m
RESET = K_r

p1 = 'Player 1'
p2 = 'Player 2'
p1Bindings = {'UP':P1UP, 'DOWN':P1DOWN}
p2Bindings = {'UP':P2UP, 'DOWN':P2DOWN}
bindingsList = {p1:p1Bindings, p2:p2Bindings}


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW 	= 	(255, 255,   0)

BALLCOLOR = WHITE
BACKGROUNDCOLOR = BLACK
PLAYERCOLOR = WHITE

bounceSound = pygame.mixer.Sound('media\\bounce2.wav')
bounceSound.set_volume(0.2)
paddleSound = pygame.mixer.Sound('media\\bounce.wav')
paddleSound.set_volume(0.2)
breakSound = pygame.mixer.Sound('media\\break.wav')
breakSound.set_volume(0.5)
icon = pygame.image.load('media\\block.png')
icon = pygame.transform.scale(icon, (128, 128))

def main():
	global screen, clock, mute, gameMode
	screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Paddle Hero!')
	pygame.display.set_icon(icon)
	clock = pygame.time.Clock()
	mute = False
	
	while True:
		gameMode = chooseGameMode()
		if gameMode == 'block':
			return
		while True:
			winner = playGame()
			if winner == 'reset':
				break
			if gameOver(winner) == 'reset':
				break

def playGame():
	global score, ball, players, mute
	score = {p1:0, p2:0}
	
	while score[p1] < SCORELIMIT and score[p2] < SCORELIMIT:
		if gameMode == 'AI':
			playerChoice = p1
		if gameMode == '2p':
			playerChoice = random.choice((p1, p2))
		players = {p1:Player(WINDOWWIDTH - (PLAYERPOS + PLAYERWIDTH), int(WINDOWHEIGHT / 2 - PLAYERHEIGHT / 2), PLAYERWIDTH, PLAYERHEIGHT),
				   p2:Player(PLAYERPOS, int(WINDOWHEIGHT / 2 - PLAYERHEIGHT / 2), PLAYERWIDTH, PLAYERHEIGHT),}
		ball = None
		if playerChoice == p1:
			ball = Ball(players[playerChoice].left - BALLSIZE, players[playerChoice].centery - BALLSIZE, BALLSIZE, BALLCOLOR)
		else:
			ball = Ball(players[playerChoice].right, players[playerChoice].centery - BALLSIZE, BALLSIZE, BALLCOLOR)
		
		if gameStart(players[playerChoice], bindingsList[playerChoice], ball) == 'reset':
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
					if event.key == K_F2:
						pygame.image.save(screen, 'image.png')
			
			players[p1], players[p1].accel, players[p1].speed = movePlayer(players[p1], players[p1].accel, players[p1].speed, p1Bindings)
			if gameMode == 'AI':
				players[p2], players[p2].accel, players[p2].speed = moveAIPlayer(players[p2], players[p2].accel, players[p2].speed, ball)
			elif gameMode == '2p':
				players[p2], players[p2].accel, players[p2].speed = movePlayer(players[p2], players[p2].accel, players[p2].speed, p2Bindings)
			#players[p2].centery = balls[0].centery
			
			ball.left += ball.dirX
			ball.top += ball.dirY
			
			if ball.left < 0: 
				breakSound.play()
				score[p1] += 1
				break
			if ball.right > WINDOWWIDTH:
				breakSound.play()
				score[p2] += 1
				break
			if ball.top < 0:
				ball.top = 0
				if not mute:
					bounceSound.play()
				ball.dirY *= -1
			if ball.bottom > WINDOWHEIGHT:
				ball.bottom = WINDOWHEIGHT
				if not mute:
					bounceSound.play()
				ball.dirY *= -1
			for p, player in players.iteritems():
				if ball.colliderect(player):
					if not mute:
						paddleSound.play()
					if p == p1:
						ball.right = player.left
					elif p == p2:
						ball.left = player.right
					factor = (MAXBALLSPEEDY*(ball.centery - player.centery)) / (PLAYERHEIGHT/2)
					ball.dirY = factor
					ball.dirX *= -1
			
			screen.fill(BACKGROUNDCOLOR)
			drawBackground(score)
			drawPlayer(players[p1])
			drawPlayer(players[p2])
			drawBall(ball)

			pygame.display.update()
			clock.tick(FPS)
	
	for player, playerScore in score.iteritems():
		if playerScore == SCORELIMIT:
			if player == p2 and gameMode == 'AI':
				return 'The Computer'
			return player

def chooseGameMode():
	topSurf = font.render('Welcome to Paddle Hero! Choose a Game Mode.', 1, WHITE)
	topRect = topSurf.get_rect()
	topRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 - 80)

	AISurf = font.render('Play Against the Computer', 1, WHITE)
	AIRect = AISurf.get_rect()
	AIRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
	
	P2Surf = font.render('Play Against a Friend', 1, WHITE)
	P2Rect = P2Surf.get_rect()
	P2Rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 50)
	
	blockSurf = font.render('Play Block Hero!', 1, YELLOW)
	blockRect = blockSurf.get_rect()
	blockRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 100)
	
	options = ('AI', '2p', 'block')
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
		screen.blit(AISurf, AIRect)
		screen.blit(P2Surf, P2Rect)
		screen.blit(blockSurf, blockRect)
		
		if options[selectedOption] == 'AI':
			pygame.draw.rect(screen, RED, AIRect, 4)
		elif options[selectedOption] == '2p':
			pygame.draw.rect(screen, RED, P2Rect, 4)
		elif options[selectedOption] == 'block':
			pygame.draw.rect(screen, RED, blockRect, 4)
		
		pygame.display.update()
		clock.tick(FPS)
		
def gameStart(player, bindings, ball):
	playerAccel = 0
	playerSpeed = 0
	while True:
		player, playerAccel, playerSpeed = movePlayer(player, playerAccel, playerSpeed, bindings)
		ball.centery = player.centery
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()
			if event.type == KEYDOWN:
				if event.key == START:
					ball.dirX = -BALLSPEEDX
					return
				if event.key == RESET:
					return 'reset'
					
		screen.fill(BLACK)
		drawBackground(score)
		drawPlayer(players[p1])
		drawPlayer(players[p2])
		drawBall(ball)
		
		textobj = smallfont.render('Press SPACE to start', 1, WHITE)
		textrect = textobj.get_rect()
		textrect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
		screen.blit(textobj, textrect)	
		
		pygame.display.update()
		clock.tick(FPS)
	
def gameOver(winner):
	screen.fill(BACKGROUNDCOLOR)
	drawText(winner + ' won the game!', font, WHITE, screen, 50, WINDOWHEIGHT/2)
	drawText('Press any key to start again.', font, WHITE, screen, 50, WINDOWHEIGHT/2 + 30)
	drawText('Or press "R" to change game modes.', font, WHITE, screen, 50, WINDOWHEIGHT/2 + 60)
	pygame.display.update()
	pygame.time.wait(1000)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()
			if event.type == KEYDOWN:
				if event.key == RESET:
					return 'reset'
				return None
		
		clock.tick(FPS)
		
def movePlayer(player, playerAccel, playerSpeed, bindings):
	keys = pygame.key.get_pressed()
	playerAccel = (keys[bindings['DOWN']] - keys[bindings['UP']]) * PLAYERACCEL

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
	#playerSpeed = 10 * playerAccel
	player.top += playerSpeed
	if player.top < 0:
		player.top = 0
		playerSpeed = 0
	if player.bottom > WINDOWHEIGHT:
		player.bottom = WINDOWHEIGHT
		playerSpeed = 0
	
	return (player, playerAccel, playerSpeed)
	
def moveAIPlayer(player, playerAccel, playerSpeed, ball):
	if ball.centery > player.top and ball.centery < player.bottom:
		playerAccel = 0
	elif ball.centery < player.top - AISTUPIDITY:
		playerAccel = -AIACCEL
	elif ball.centery > player.bottom + AISTUPIDITY:
		playerAccel = AIACCEL

	if playerAccel != 0:
		if playerSpeed != MAXAISPEED and playerSpeed != -MAXAISPEED:
			playerSpeed += playerAccel
			if playerSpeed > MAXAISPEED:
				playerSpeed = MAXAISPEED
			if playerSpeed < -MAXAISPEED:
				playerSpeed = -MAXAISPEED

	if playerAccel == 0:
		if playerSpeed > 0:
			playerSpeed -= AIDEACCEL
			if playerSpeed < 0:
				playerSpeed = 0
		if playerSpeed < 0:
			playerSpeed += AIDEACCEL
			if playerSpeed > 0:
				playerSpeed = 0
				
	player.top += playerSpeed
	if player.top < 0:
		player.top = 0
		playerSpeed = 0
	if player.bottom > WINDOWHEIGHT:
		player.bottom = WINDOWHEIGHT
		playerSpeed = 0
	
	return (player, playerAccel, playerSpeed)
				
def drawBackground(score):
	lineHeight = int(WINDOWHEIGHT/30)
	for i in range(30):
		if i % 2 == 0:
			pygame.draw.line(screen, WHITE, (WINDOWWIDTH/2, i * lineHeight), (WINDOWWIDTH/2, i * lineHeight + lineHeight), 4)
		else:
			pygame.draw.line(screen, BLACK, (WINDOWWIDTH/2, i * lineHeight), (WINDOWWIDTH/2, i * lineHeight + lineHeight), 4)
		
	drawText(str(score[p2]), font, WHITE, screen, WINDOWWIDTH/2 - 20, 30)
	drawText(str(score[p1]), font, WHITE, screen, WINDOWWIDTH/2 + 10, 30)
	
def drawPlayer(player):
	pygame.draw.rect(screen, PLAYERCOLOR, player)
	
def drawBall(ball):
	pygame.draw.rect(screen, ball.color, ball)
		
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
					
def drawText(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)
font = pygame.font.SysFont("Arial", 30)
smallfont = pygame.font.SysFont("Arial", 15)

def terminate():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()