# Import and initialize the pygame library
import pygame
import random
import json
import sys
import os

from helper_module import mykwargs



# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)




def assignVariables():
    WIDTH = 500
    HEIGHT = 500
    PWIDTH = 50
    PHEIGHT = 50
    TITLE = 'Covid Game!'

    argv = sys.argv[1:]
    #Collect all args and kwargs from command console :)
    args,kwargs = mykwargs(argv)
    kwargs =  {k.lower(): v for k, v in kwargs.items()}
    for key,value in kwargs.items():
        print(key)
        if key == 'width':
            WIDTH = int(value)
        if key == 'height':
            HEIGHT = int(value)
        if key == 'pheight':
            PHEIGHT = int(value)
        if key == 'pwidth':
            PWIDTH = int(value)
        if key == 'title':
            TITLE = value
    return WIDTH,HEIGHT,PWIDTH,PHEIGHT,TITLE
    
    
class Player:
    def __init__(self,screen,image,x,y,PWIDTH,PHEIGHT,WIDTH,HEIGHT):
        self.image = image
        self.screen = screen
        self.x = x/2
        self.y = y-PHEIGHT
        self.dx = 0
        self.dy = 0
        self.speed = 1
        self.last_direction = None
        self.w = WIDTH
        self.h = HEIGHT
        self.pwit = PWIDTH
        self.phit = PHEIGHT

    def Draw(self):
        self.screen.blit(self.image, (self.x, self.y))


    def OnWorld(self):
        w, h = pygame.display.get_surface().get_size()

        return self.x > 0 and self.x < w and self.y > 0 and self.y < h

    def GetDirection(self,keys):
        if keys[K_UP]:
            return K_UP
        elif keys[K_DOWN]:
            return K_DOWN
        elif keys[K_LEFT]:
            return K_LEFT
        elif keys[K_RIGHT]:
            return K_RIGHT
        return None

    def Move(self,keys):
        direction = self.GetDirection(keys)
        if self.OnWorld() or direction != self.last_direction:
            if keys[K_UP]:
                self.y -= self.speed
                self.last_direction = K_UP
            elif keys[K_DOWN] and self.y < self.h-self.phit:
                self.y += self.speed
                self.last_direction = K_DOWN
            elif keys[K_LEFT]:
                self.x -= self.speed
                self.last_direction = K_LEFT
            elif keys[K_RIGHT] and self.x < self.w-self.pwit:
                self.x += self.speed
                self.last_direction = K_RIGHT

def main():
        
    WIDTH,HEIGHT,PWIDTH,PHEIGHT,TITLE = assignVariables()
    

    pygame.init()
    
    # sets the window title
    pygame.display.set_caption(TITLE)

    # set circle locaton
    width = WIDTH
    height = HEIGHT

    # Set up the drawing window
    screen = pygame.display.set_mode((width,height))
    image = pygame.image.load(r'C:\Users\Landen\OneDrive\Desktop\A05.1\redSquare.png')
    image = pygame.transform.scale(image,(PWIDTH,PHEIGHT))
    # construct the ball
    b1 = Player(screen,image,WIDTH,HEIGHT, PWIDTH, PHEIGHT, WIDTH, HEIGHT)

    # Run until the user asks to quit
    # game loop
    running = True
    while running:

        screen.fill((88,88,88))

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # in a minute
        pressed_keys = pygame.key.get_pressed()
        b1.Move(pressed_keys)

        b1.Draw()

        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    main()
