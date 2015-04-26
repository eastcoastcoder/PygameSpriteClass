'''
#PygameSpriteClass
The goal of this assignment is to create a functioning generic sprite class.  
When I say generic, I mean that the functionality of the class can be provided to any game entity that 
requires it either through inheritance or through inclusion of a sprite object.

#Basic (B level specifications):

**Draw command**

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

screen = pygame.display.set_mode((SCREEN_WD_HT, SCREEN_WD_HT)) 
 
class SpriteLoader(object):
    
    def __init__(self, name, mode):
        """Constructor"""
        #pygame.sprite.Sprite.__init__(self)
        self.animation = []
        self.STOP = 0
        self.PLAY = 1
        self.PAUSED = 2
                
        if(mode == 'Dir'):
            self.loadMultiFile(name)
        elif(mode == 'Sheet'):
            self.loadSpriteSheet(name)

        self.sprite = self.stopFrame
        self.drawFrame = 0
        self.state = self.STOP
        self.pause = 0
        
        self.width = self.sprite.get_width()       
        self.height = self.sprite.get_height() 
                   
    def loadMultiFile(self, dirName):
        """Load from multiple graphic files"""
        self.stopFrame = pygame.image.load(dirName + "00.bmp")
        self.stopFrame = self.stopFrame.convert()
        
        dirScan = glob(dirName + "*.*")
        for i in range(1,len(dirScan)):
            animFrame = dirScan[i]
            tempFrame = pygame.image.load(animFrame)
            tempFrame = tempFrame.convert()
            self.animation.append(tempFrame)
            
    def loadSpriteSheet(self, fileName):
        """Load from sprite sheets"""
        self.fileName = fileName
        self.image = pygame.image.load(fileName).convert()
        pass
    
    def draw(self, delay, transColor):
        self.__setTransColor(transColor)
        
        if self.state == self.STOP:
            self.sprite = self.stopFrame
        else:
            self.pause += 1
            if self.pause > delay:
                self.pause = 0
                
                #Pauses Animation
                if(self.state == self.PAUSED):
                    self.drawFrame = self.drawFrame
                    
                else:
                    self.drawFrame += 1
                
                    #Stops Animation
                    if self.drawFrame >= len(self.animation):
                        self.drawFrame = 0
                        self.state = self.STOP
                        self.sprite = self.stopFrame
                    
                    #Plays Animation
                    else:
                        self.sprite = self.animation[self.drawFrame]
                        
            
        '''
        - set animation range through a start drawFrame and end drawFrame
        - specify a current animation drawFrame
        - return which animation drawFrame the animation is currently in
        - helper functions as needed
        '''
    
    def __setTransColor(self, transColor):
        """Sets Sprite's Transparent Color"""
        self.stopFrame.set_colorkey(transColor)
        for i in range(len(self.animation)):
            self.animation[i].set_colorkey(transColor)      
                      
    def rotate(self, angle):
        """Rotates Sprite"""
        self.stopFrame = pygame.transform.rotate(self.stopFrame, angle)
        for i in range(len(self.animation)):
            self.animation[i] = pygame.transform.rotate(self.animation[i], angle)
    
    def resizeSprite(self, objective, factor):
        """Resizes Sprite"""
        if(objective == 'Scale'):
            self.width *= factor
            self.height *= factor
        elif(objective == 'Shrink'):
            self.width /= factor
            self.height /= factor
        
        self.stopFrame = pygame.transform.scale(self.stopFrame, (self.width,self.height))
        for i in range(len(self.animation)):
            self.animation[i] = pygame.transform.scale(self.animation[i], (self.width,self.height))
    
    def getWidth(self):
        """Returns Current Width of Sprite"""
        return self.width
    
    def getHeight(self):
        """Returns Current Height of Sprite"""
        return self.height
        
def main():
    
    spriteObj = SpriteLoader('assets/cow/', 'Dir')
    #spriteSheetObj = SpriteLoader('assets/cow/', 'Sheet', (111, 79, 51, 255))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    
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
                    if (spriteObj.state == spriteObj.STOP):
                        spriteObj.state = spriteObj.PLAY
                        print "Playing"
                    elif (spriteObj.state == spriteObj.PLAY):    
                        spriteObj.state = spriteObj.PAUSED
                        print "Pausing"
                    elif (spriteObj.state == spriteObj.PAUSED):    
                        spriteObj.state = spriteObj.PLAY    
                        print "Resuming"
                        
                if event.key == pygame.K_UP:
                    spriteObj.resizeSprite('Scale', 2)
                    print "Scale Up"
                if event.key == pygame.K_DOWN:
                    spriteObj.resizeSprite('Shrink', 2)
                    print "Shrink Down"
                if event.key == pygame.K_LEFT:
                    spriteObj.rotate(90)
                    print "Rotate Left"
                if event.key == pygame.K_RIGHT:
                    spriteObj.rotate(-90)
                    print "Rotate Right"
                    
        spriteObj.draw(3, (111, 79, 51, 255))
        screen.blit(spriteObj.sprite, (100,100))
        msElapsed = clock.tick(30)
        pygame.display.update() 
    
if __name__ == '__main__':
    main()
    