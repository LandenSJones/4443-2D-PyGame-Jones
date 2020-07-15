#Landen Jones

#Imports
#--------------------
import pygame
import random
#--------------------

#--------------------
WIDTH = 640
HEIGHT = 480
WIDTHPLAYER = 50
HEIGHTPLAYER = 50
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    #Sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     #Pygames basic sprite constructor
        self.image = pygame.Surface((WIDTHPLAYER, HEIGHTPLAYER))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()       #looks at the image and figures out what the image rect needs to be
        self.rect.center = (WIDTH/2, HEIGHT - HEIGHTPLAYER/2)  #sets center of image at the center of the screen
    def update(self):
        self.rect.x += 5
#--------------------

#Creates the window :)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MY GAME TITLE")
clock = pygame.time.Clock()

allSprites = pygame.sprite.Group()
player = Player()
allSprites.add(player)

#Game Loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update
    allSprites.update()
    #Draw            
    screen.fill(BLACK)
    allSprites.draw(screen)
    
    pygame.display.flip()

pygame.quit()
