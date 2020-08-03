#Landen Jones
#Import Necessary Modules
import pygame
import sys
import os
import random
import math
from os import path

imgDir = path.join(path.dirname(__file__), 'media')
sndDir = path.join(path.dirname(__file__), 'snd')
#Default Variables
windowWidth = 800
windowHeight = 600
windowName = "Presentation Video!"
fps = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)


#Import pygame.locals for easier access to key coordinates
#Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_w,
    K_DOWN,
    K_s,
    K_LEFT,
    K_a,
    K_RIGHT,
    K_d,
    K_ESCAPE,
    K_SPACE,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    KEYDOWN,
    KEYUP,
    QUIT,
)

def mykwargs(argv):
    '''
    Processes argv list into plain args and kwargs.
    Just easier than using a library like argparse for small things.
    Example:
        python file.py arg1 arg2 arg3=val1 arg4=val2 -arg5 -arg6 --arg7
        Would create:
            args[arg1, arg2, -arg5, -arg6, --arg7]
            kargs{arg3 : val1, arg4 : val2}

        Params with dashes (flags) can now be processed seperately
    Shortfalls:
        spaces between k=v would result in bad params
    Returns:
        tuple  (args,kargs)
    '''
    args = []
    kargs = {}
    for arg in argv:
        if '=' in arg:
            key,val = arg.split('=')
            kargs[key] = val
        else:
            args.append(arg)
    return args,kargs

font_name = pygame.font.match_font('arial') 
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerImg, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = windowWidth / 2
        self.rect.bottom = windowHeight -20
        self.speedx = 0
        self.speedy = 0
        
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed() #gets all keys that are pressed
        if keystate[K_a]:
            self.speedx = -2
        if keystate[K_d]:
            self.speedx = +2
        if keystate[K_w]:
            self.speedy = -2
        if keystate[K_s]:
            self.speedy = +2
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > windowWidth:
            self.rect.right = windowWidth
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > windowHeight:
            self.rect.bottom = windowHeight
        if self.rect.top < 0:
            self.rect.top = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        allSprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bulletImg, (10,5))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.radius = 5
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centery = y
        self.rect.centerx = x
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX = mouseX - x
        mouseY = mouseY - y
        self.speedx, self.speedy = self.Angle(mouseX, mouseY)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #Kill if moves off of top of screen
        if self.rect.bottom < 0:
            self.kill() #removes sprite from any groups and kills it
        if self.speedx == 0 and self.speedy ==0:
            self.kill()
    def Angle(self, x, y):
        if x == 0:
            x = 1
        if y == 0:
            y = 1
        x = int(x/100)
        y = int(y/100)
        return int(x), int(y)
    
    

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imageOrig = random.choice(meteorImages)
        self.image = self.imageOrig.copy()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.imageOrig.set_colorkey(BLACK)
        self.radius = int(self.rect.width * .85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(windowWidth - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 3)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rotSpeed = random.randrange(-8, 8)
        self.lastUpdate = pygame.time.get_ticks()
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > 50:
            self.lastUpdate = now
            self.rot = (self.rot + self.rotSpeed) % 360
            newImage = pygame.transform.rotate(self.imageOrig, self.rot)
            oldCenter = self.rect.center
            self.image = newImage
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > windowHeight + 10 or self.rect.left < -20 or self.rect.right > windowWidth + 20:        #If it leaves through the bottom, then respawn
            self.rect.x = random.randrange(windowWidth - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 2)


    

#Gets command line parameters
argv = sys.argv[1:]
args,kwargs = mykwargs(argv)

#Initializes pygame and the sound
pygame.init()
pygame.mixer.init()



#Gives screen dimentions and a window name
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption(windowName)
clock = pygame.time.Clock()

#Load all game graphics and sounds
shoot_sound = pygame.mixer.Sound(path.join(sndDir, 'laser.wav'))
shoot_sound.set_volume(0.4)
explosion_sound = pygame.mixer.Sound(path.join(sndDir, 'explosion.wav'))
explosion_sound.set_volume(0.4)
pygame.mixer.music.load(path.join(sndDir, 'spacemusic.mp3'))
pygame.mixer.music.set_volume(0.4)
background = pygame.image.load(path.join(imgDir, "starfield.png")).convert()
backgroundRect = background.get_rect()
playerImg = pygame.image.load(path.join(imgDir, "playerShip1_orange.png")).convert()
meteorImg = pygame.image.load(path.join(imgDir, "meteorBrown_med1.png")).convert()
bulletImg = pygame.image.load(path.join(imgDir, "laserRed16.png")).convert()
meteorImages = []
meteorList =['meteorBrown_big1.png','meteorBrown_big2.png','meteorBrown_big3.png','meteorBrown_big4.png',
             'meteorBrown_med1.png','meteorBrown_med3.png',
             'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png']
for img in meteorList:
    meteorImages.append(pygame.image.load(path.join(imgDir, img)).convert())
#Creates an empty group sprites, we're going to put all sprites in this group
allSprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
allSprites.add(player)
for i in range(8):
    m = Mob()
    allSprites.add(m)
    mobs.add(m)
score = 0
pygame.mixer.music.play(loops = -1)
#Game Loop
running = True
while running:
    #Keep running at the right speed (FPS)
    clock.tick(fps)
    
    #Process input (events)
    for event in pygame.event.get():
        if (event.type == QUIT):
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot()
    #Update
    allSprites.update()
    #Check to see if any bullet hits the mobs
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) #(Group of mob, group of mob, if 1st is deleted?, is 2nd deleted)
    for hit in hits:
        explosion_sound.play()
        score +=  50 - hit.radius
        m = Mob()
        allSprites.add(m)
        mobs.add(m)
    #Check to see if a mob hit the player, hits will hold mobs that hit the player, or vice verse
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)  #(Which Sprite, Which Group, If should be deleted)
    if hits:
        running = False
    
    #Draw / render
    screen.fill(BLACK)
    screen.blit(background, backgroundRect)
    allSprites.draw(screen)
    draw_text(screen, str(score), 18, windowWidth / 2, 10)
    #After drawing everything, flip the display
    pygame.display.flip()

    
pygame.quit()

