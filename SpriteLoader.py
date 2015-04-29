'''
#PygameSpriteClass
The goal of this assignment is to create a functioning generic curFrame class.  
When I say generic, I mean that the functionality of the class can be provided to any game entity that 
requires it either through inheritance or through inclusion of a curFrame object.

#Basic (B level specifications):

**Animation commands**
 - set animation range through a start drawFrame and end drawFrame
 - specify a current animation drawFrame
 - return which animation drawFrame the animation is currently in

#Advanced (A level specifications):

 - Fix the surface scaling problem with the Rotate command
 - Allow the user to create specific animations that are easily loaded 
 - Manipulate alpha to make curFrame partially transparent
 - Debug mode that shows borders and animation frames
'''

import pygame, sys, os
from glob import *
 
pygame.init()
clock = pygame.time.Clock()

SCREEN_WD_HT = 800

screen = pygame.display.set_mode((SCREEN_WD_HT, SCREEN_WD_HT)) 
 
class SpriteLoader(object):
    
    def __init__(self):
        """Constructor"""
        self.animation = []
        self.state = 'STOP'
        self.drawFrame = 0
        self.speed = 0
        self.delay = 3
        
    def loadMultiFile(self, dirName):
        """Load from Multiple Sprite Files"""
        self.stopFrame = pygame.image.load(dirName + "00.bmp").convert()
        
        dirScan = glob(dirName + "*.*")
        for i in range(1,len(dirScan)):
            animFrame = dirScan[i]
            tempFrame = pygame.image.load(animFrame)
            tempFrame = tempFrame.convert()
            self.animation.append(tempFrame)
            
        self.curFrame = self.stopFrame
        self.width = self.curFrame.get_width()
        self.height = self.curFrame.get_height() 
           
    def loadSpriteSheet(self, fileName, start, size, columns, rows):
        """Load from Single Sprite Sheet"""
        spriteSheet = pygame.image.load(fileName).convert()
        
        for j in range(rows):
            for i in range(columns):
                location = (start[0]+size[0]*i, start[1]+size[1]*j)
                if (location == (0,0)):
                    self.stopFrame = spriteSheet.subsurface(pygame.Rect(location,size))
                else:
                    self.animation.append(spriteSheet.subsurface(pygame.Rect(location,size)))
        
        self.curFrame = self.stopFrame
        self.width = self.curFrame.get_width()
        self.height = self.curFrame.get_height()         
        
    #Start: should be 
    #End:   should be    
    #def animate(self, delay, start, end):
    def animate(self):
        """Loops Sprite Animation"""
        if self.state == 'STOP':
            self.curFrame = self.stopFrame
        else:
            self.speed += 1
            
            #Sets up Animation Speed
            if self.speed > self.delay:
                self.speed = 0
                
                #Pauses Animation
                if(self.state == 'PAUSED'):
                    self.drawFrame = self.drawFrame
                #Plays Animation    
                else:
                    self.drawFrame += 1
                
                    #Stops Animation
                    if self.drawFrame >= len(self.animation):
                        self.drawFrame = 0
                        self.state = 'STOP'
                        self.curFrame = self.stopFrame
                    
                    #Draws Animation
                    else:
                        self.curFrame = self.animation[self.drawFrame]
    
    def setTransColor(self, transColor):
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
        """
        Resizes Sprite
        Caution: This is Lossy!
        """
        if(objective == 'Scale'):
            self.width *= factor
            self.height *= factor
        elif(objective == 'Shrink'):
            self.width /= factor
            self.height /= factor
        
        self.stopFrame = pygame.transform.scale(self.stopFrame, (self.width,self.height))
        for i in range(len(self.animation)):
            self.animation[i] = pygame.transform.scale(self.animation[i], (self.width,self.height))
    
    #Mutators
    def playAnimation(self):
        """Sets State Flag to PLAY"""
        self.state = 'PLAY'
    
    def pauseAnimation(self):
        """Sets State Flag to PAUSED"""
        self.state = 'PAUSED'    
    
    def setAnimationDelay(self, delay):
        """
        Sets Animation Delay
        Default Delay: 3
        """
        self.delay = delay
    
    #Accessors
    def getWidth(self):
        """Returns Current Width of Sprite"""
        return self.width
    
    def getHeight(self):
        """Returns Current Height of Sprite"""
        return self.height
    
    def getState(self):
        """Returns State Flag"""
        return self.state
        
def main():
    
    spriteObj = SpriteLoader()
    
    #Uncomment for Multiple File cow
    #spriteObj.loadMultiFile('assets/cow/')

    #Uncomment for SpriteSheet file cow
    #spriteObj.loadSpriteSheet("assets/COWABUNGA.bmp", [0,0], [96,96], 12, 1)
    
    #Uncomment for Cow TransColor
    #spriteObj.setTransColor((111, 79, 51, 255))    
    
    #Uncomment for SpriteSheet file asteroid
    spriteObj.loadSpriteSheet("assets/asteroid.bmp", [0,0], [64,64], 8, 8)
    spriteObj.setTransColor((255, 0, 255, 255))
    
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
                    if (spriteObj.getState() == 'STOP'):
                        spriteObj.playAnimation()
                    elif (spriteObj.getState() == 'PLAY'):    
                        spriteObj.pauseAnimation()
                    elif (spriteObj.getState() == 'PAUSED'):    
                        spriteObj.playAnimation() 
                    print spriteObj.getState()
                        
                if event.key == pygame.K_UP:
                    spriteObj.resizeSprite('Scale', 2)
                    print "Scale Up (", spriteObj.getWidth(), ",", spriteObj.getHeight(), ")" 
                if event.key == pygame.K_DOWN:
                    spriteObj.resizeSprite('Shrink', 2)
                    print "Shrink Down (", spriteObj.getWidth(), ",", spriteObj.getHeight(), ")"
                if event.key == pygame.K_LEFT:
                    spriteObj.rotate(90)
                    print "Rotate Left"
                if event.key == pygame.K_RIGHT:
                    spriteObj.rotate(-90)
                    print "Rotate Right"
                    
        spriteObj.setAnimationDelay(3)            
        spriteObj.animate()
        
        screen.blit(spriteObj.curFrame, (100,100))
        msElapsed = clock.tick(30)
        pygame.display.update() 
    
if __name__ == '__main__':
    main()
    