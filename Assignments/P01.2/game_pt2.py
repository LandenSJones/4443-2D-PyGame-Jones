#Landen Jones
# Import Necessary Modules
import pygame
import sys
import os

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

class Scene(pygame.sprite.Sprite):
    def __init__(self,backgroundImg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(backgroundImg)
        self.scene_rect = self.image.get_rect()
    def draw(self,screen):
        screen.blit(self.image,self.scene_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self,screen,scene,imgUp,imgDown,imgLeft,imgRight):
        pygame.sprite.Sprite.__init__(self)
        self.playerImages = [imgUp,imgDown,imgLeft,imgRight]
        self.image = pygame.image.load(self.playerImages[0])
        self.scene_rect = scene
        self.screenDim = screen.get_rect()
        self.playerDim = self.image.get_rect()
        self.playerDim.centerx = self.screenDim.centerx
        self.playerDim.centery = self.screenDim.centery
        self.speed = 1
        
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.flash = False #Shows alive
        
    def Move(self):
        for event in pygame.event.get():
            if (event.type == QUIT):
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.up = True
                    self.image = pygame.image.load(self.playerImages[0])
                elif event.key == K_DOWN:
                    self.down = True
                    self.image = pygame.image.load(self.playerImages[1])
                elif event.key == K_LEFT:
                    self.left = True
                    self.image = pygame.image.load(self.playerImages[2])
                elif event.key == K_RIGHT:
                    self.right = True
                    self.image = pygame.image.load(self.playerImages[3])
            elif event.type == KEYUP:
                if event.key == K_UP:
                    self.up = False
                elif event.key == K_DOWN:
                    self.down = False
                elif event.key == K_LEFT:
                    self.left = False
                elif event.key == K_RIGHT:
                    self.right = False
                    
    def Collision(self,scene):
        if (self.scene_rect.x <= -1575 or self.scene_rect.x >= 295 or self.scene_rect.y <= -450 or self.scene_rect.y >= 200):
            return True
        else:
            return False
            
    def update(self,scene):
        if self.up and self.playerDim.top > self.scene_rect.top:
            self.scene_rect.centery += self.speed
        if self.down and self.playerDim.bottom < self.scene_rect.bottom:
            self.scene_rect.centery -= self.speed
        if self.left and self.playerDim.left > self.scene_rect.left:
            self.scene_rect.centerx += self.speed
        if self.right and self.playerDim.right < self.scene_rect.right:
            self.scene_rect.centerx -= self.speed
            
    def draw(self,window):
        window.blit(self.image,(self.playerDim))
    

def Game():
    #Initialize default values
    winWei = 640
    winHei = 480
    title = "Default Title"
    backgroundImg = " "
    imgUp = " "
    imgDown = " "
    imgLeft = " "
    imgRight = " "
    #Gives  color values to Black and White
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    argv = sys.argv[1:]
    args,kwargs = mykwargs(argv)
    #Extracts necessary information from command parameters
    for key,value in kwargs.items():
        if(key == "imgU"):
            imgUp = value
        elif(key == "imgD"):
            imgDown = value
        elif(key == "imgL"):
            imgLeft = value
        elif(key == "imgR"):
            imgRight = value
        elif(key == "height"):
            winHei = int(value)
        elif(key == "width"):
            winWei = int(value)
        elif(key == "title"):
            title = value
        elif(key == "background"):
            backgroundImg = value
    
    #Sets background color to white.
    BG = WHITE
    
    #Initializes pygame window
    pygame.init()
    window = pygame.display.set_mode((winWei,winHei))
    pygame.display.set_caption(title)
    
    scene = Scene(backgroundImg)
    
    #Create Player with command entered command parameteres
    player = Player(window,scene.scene_rect,imgUp,imgDown,imgLeft,imgRight)
    
    #Game plays here
    while True:
        window.fill(BG)  #Fill background of camera window to WHITE
        scene.draw(window)
        player.Move()  #Checks for key inputs
        
        #If player collides with end of scene the turn the background color to black
        if(player.Collision(scene)):
            BG = BLACK
        
        player.update(scene)
        player.draw(window)
        pygame.display.flip()
            


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



def main():
    Game()
    
if __name__=='__main__':
    main()
