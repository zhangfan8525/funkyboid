import pygame, sys, random
from pygame.locals import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRAVITY = 20
SCORE = 0

BRICK_NUMBER = 10
BRICK_SIZE = WINDOW_HEIGHT / BRICK_NUMBER
WALL_X = WINDOW_WIDTH
GAP_SIZE = 3

BOID_RADIUS = 20
BOID_X = BRICK_SIZE	
BOID_Y = WINDOW_HEIGHT / 2
BOID_VELO_X = 0
BOID_VELO_Y = 0

BLUE = (0, 0, 255)
GALAXY_IMG = pygame.image.load("galaxy.jpg")
SPACESHIP_IMG = pygame.image.load("spaceship.png")
PLANET_IMG = pygame.image.load("planet.png")

def main():
	global FPSCLOCK, DISPLAYSURF, FPS, BOID_VELO_X, BOID_VELO_Y,BOID_X, BOID_Y, BOID_RADIUS, SCORE, WALL_X
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("FUNKY BOID (Game of the Year Edition)")

	wall = randomWall()
	while True:
		DISPLAYSURF.blit(GALAXY_IMG, (0, 0))

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					BOID_VELO_Y = -50;
				elif event.key == K_LEFT:
					BOID_VELO_X -= 20
				elif event.key == K_RIGHT:
					BOID_VELO_X += 20
		
		if (BOID_Y >= (WINDOW_HEIGHT - BOID_RADIUS / 2) and BOID_VELO_Y > 0) or (BOID_Y <= BOID_RADIUS and BOID_VELO_Y < 0):
			BOID_VELO_Y = -BOID_VELO_Y
		if ((BOID_X + BOID_RADIUS / 2) >= WINDOW_WIDTH and BOID_VELO_X > 0) or ((BOID_X - BOID_RADIUS / 2) <= 0 and BOID_VELO_X < 0):
			BOID_VELO_X = -BOID_VELO_X

		if BOID_Y > WINDOW_HEIGHT - BOID_RADIUS / 2:
			updateBoidPos(-BOID_VELO_X / 6, GRAVITY, 0.3)
		else:
			updateBoidPos(-BOID_VELO_X / 60, GRAVITY, 0.3)

		wall = advanceWall(wall)

		if hitWall(wall):
			pygame.time.wait(1000)
			reset()

		drawWall(wall)
		drawBoid(BOID_X, BOID_Y)
		drawScore()
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def updateBoidPos(accelX, accelY, deltaTime):
	global BOID_X, BOID_Y, BOID_VELO_X, BOID_VELO_Y, BOID_RADIUS
	BOID_VELO_X += accelX * deltaTime
	BOID_VELO_Y += accelY * deltaTime

	if abs(BOID_VELO_X) > 5 or abs(accelX) > 0.1:
		BOID_X += BOID_VELO_X * deltaTime + accelX * deltaTime * deltaTime / 2
	BOID_Y += BOID_VELO_Y * deltaTime + accelY * deltaTime * deltaTime / 2
	if BOID_Y > WINDOW_HEIGHT - BOID_RADIUS / 2:
		BOID_Y = WINDOW_HEIGHT - BOID_RADIUS / 2

def drawBoid(x, y):
	DISPLAYSURF.blit(SPACESHIP_IMG, (int(x), int(y)))

def randomWall():
	result = [1] * 10
	random.seed()
	gapStart = random.randint(0, BRICK_NUMBER - GAP_SIZE)
	result[gapStart:gapStart + GAP_SIZE] = [0] * GAP_SIZE
	print(result)
	return result

def advanceWall(wall):
	global WALL_X, SCORE
	WALL_X -= WINDOW_WIDTH / (FPS * 4) 
	if(WALL_X < -BRICK_SIZE):
		wall = randomWall()
		WALL_X = WINDOW_WIDTH
		SCORE = SCORE + 1
	return wall

def drawWall(wall):
	for idx, val in enumerate(wall): 
		if val:
			DISPLAYSURF.blit(PLANET_IMG, (WALL_X, idx * BRICK_SIZE))

def drawScore():
	fontObj = pygame.font.Font("freesansbold.ttf", int(BRICK_SIZE))
	textSurfaceObj = fontObj.render(str(SCORE), False, BLUE)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (BRICK_SIZE, BRICK_SIZE)
	DISPLAYSURF.blit(textSurfaceObj, textRectObj)
	
def hitWall(wall):
	boidRect = pygame.Rect(BOID_X, BOID_Y, 2 * BOID_RADIUS, 2 * BOID_RADIUS)
	for idx, val in enumerate(wall):
		if val:
			brickRect = pygame.Rect(WALL_X, idx * BRICK_SIZE, BRICK_SIZE, BRICK_SIZE)
			if boidRect.colliderect(brickRect):
				return True
	return False

def reset():
	global SCORE, WALL_X, BOID_X, BOID_Y, BOID_VELO_X, BOID_VELO_Y
	SCORE = 0
	WALL_X = WINDOW_WIDTH	
	BOID_X = BRICK_SIZE	
	BOID_Y = WINDOW_HEIGHT / 2
	BOID_VELO_X = 0
	BOID_VELO_Y = 0

if __name__ == "__main__":
	main()

