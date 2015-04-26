'''
#PygameSpriteClass
The goal of this assignment is to create a functioning generic sprite class.  
When I say generic, I mean that the functionality of the class can be provided to any game entity that 
requires it either through inheritance or through inclusion of a sprite object.

#Basic (B level specifications):

**Draw command**

 - Specify a transparent color

**Animation commands**
 
 - play/pause animation
 - change animation delay
 - set animation range through a start drawFrame and end drawFrame
 - specify a current animation drawFrame
 - return which animation drawFrame the animation is currently in
 - helper functions as needed
Rotate sprite
Scale sprite
 - Should be able to resize up and down
Get Width and Height (remember scaling)

#Advanced (A level specifications):

 - Fix the surface scaling problem with the Rotate command
 - Allow the user to create specific animations that are easily loaded 
 - Manipulate alpha to make sprite partially transparent
 - Debug mode that shows borders and animation frames
'''
import pygame, sys, os
from glob import *
 
pygame.init()
clock = pygame.time.Clock()

SCREEN_WD_HT = 800
SCALING_FACTOR = 2

screen = pygame.display.set_mode((SCREEN_WD_HT, SCREEN_WD_HT)) 
 
class SpriteLoader(pygame.sprite.Sprite):
    
    def __init__(self, dirName, transColor):
        """Constructor"""
        pygame.sprite.Sprite.__init__(self)
        self.animation = []
        self.STOP = 0
        self.MOOING = 1
        self.width = 0
        self.height = 0
        self.resize = 1
        self.transColor = transColor
        
        self.loadMultiFile(dirName)
        self.sprite = self.stopFrame
        self.drawFrame = 0
        self.state = self.STOP
        
        self.pause = 0
        self.delay = 3
        
    def loadMultiFile(self, dirName):
        """Load from multiple graphic files"""
        self.stopFrame = pygame.image.load(dirName + "00.bmp")
        self.stopFrame = self.stopFrame.convert()
        self.stopFrame.set_colorkey(self.transColor)
        
        dirScan = glob(dirName + "*.*")
        for i in range(1,len(dirScan)):
            animFrame = dirScan[i]
            tempFrame = pygame.image.load(animFrame)
            tempFrame = tempFrame.convert()
            tempFrame.set_colorkey(self.transColor)
            self.animation.append(tempFrame)
            
    def loadSpriteSheet(self, fileName):
        """Load from sprite sheets"""
        self.fileName = fileName
        self.image = pygame.image.load(fileName).convert()
        pass
    
    def draw(self, color, surface):
        """Specify a transparent color"""
        self.transparent = color;
        transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(transColor)
        #pygame.draw
    
        '''
        - play/pause animation
        - change animation delay
        - set animation range through a start drawFrame and end drawFrame
        - specify a current animation drawFrame
        - return which animation drawFrame the animation is currently in
        - helper functions as needed
        '''
    
    def update(self):
        if self.state == self.STOP:
            self.sprite = self.stopFrame
        else:
            self.pause += 1
            if self.pause > self.delay:
                self.pause = 0
                self.drawFrame += 1
                if self.drawFrame >= len(self.animation):
                    self.drawFrame = 0
                    self.state = self.STOP
                    self.sprite = self.stopFrame
                else:
                    self.sprite = self.animation[self.drawFrame]

    def rotate(self, angle):
        self.stopFrame = pygame.transform.rotate(self.stopFrame, angle)
        for i in range(len(self.animation)):
            self.animation[i] = pygame.transform.rotate(self.animation[i], angle)
    
    def resizeSprite(self, objective):
        """Resizes Sprite"""
        if(objective == 'scale'):
            wid = self.sprite.get_width()*SCALING_FACTOR
            ht = self.sprite.get_height()*SCALING_FACTOR
        elif(objective == 'shrink'):
            wid = self.sprite.get_width()/SCALING_FACTOR
            ht = self.sprite.get_height()/SCALING_FACTOR
            
        self.stopFrame = pygame.transform.scale(self.stopFrame, (wid,ht))
        for i in range(len(self.animation)):
            self.animation[i] = pygame.transform.scale(self.animation[i], (wid,ht))
        
    def getWidth(self):
        return self.width*self.resize
    
    def getHeight(self):
        return self.height*self.resize

def main():
    
    spriteObj = SpriteLoader('assets/cow/', (111, 79, 51, 255))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    
    background.blit(background, (0, 0))
    
    while(True):
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spriteObj.state = spriteObj.MOOING
                if event.key == pygame.K_UP:
                    spriteObj.resizeSprite('scale')
                if event.key == pygame.K_DOWN:
                    spriteObj.resizeSprite('shrink')
                if event.key == pygame.K_LEFT:
                    spriteObj.rotate(90)
                if event.key == pygame.K_RIGHT:
                    spriteObj.rotate(-90)
        
        screen.blit(spriteObj.sprite,(100,100))
        spriteObj.update()
        msElapsed = clock.tick(30)
        pygame.display.update() 
    
if __name__ == '__main__':
    main()
    