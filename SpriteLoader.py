'''
#PygameSpriteClass
The goal of this assignment is to create a functioning generic curFrame class.  
When I say generic, I mean that the functionality of the class can be provided to any game entity that 
requires it either through inheritance or through inclusion of a curFrame object.

#Basic (B level specifications):

**Animation commands**
 - play/pause animation
 - change animation delay
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
        self.pause = 0
        
    def loadMultiFile(self, dirName):
        """Load from multiple graphic files"""
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
           
    def loadSpriteSheet(self, fileName, start, size, columns, rows=1):
        """Load from curFrame sheets"""
        spriteSheet = pygame.image.load(fileName).convert()
        
        for j in range(rows):
            for i in range(columns):
                location = (start[0]+size[0]*i, start[1]+size[1]*j)
                print location
                if (location == (0,0)):
                    self.stopFrame = spriteSheet.subsurface(pygame.Rect(location,size))
                else:
                    self.animation.append(spriteSheet.subsurface(pygame.Rect(location,size)))
        
        self.curFrame = self.stopFrame
        
        self.width = self.curFrame.get_width()
        self.height = self.curFrame.get_height()         
        
    def draw(self, delay, transColor):
        self.__setTransColor(transColor)
        
        if self.state == 'STOP':
            self.curFrame = self.stopFrame
        else:
            self.pause += 1
            if self.pause > delay:
                self.pause = 0
                
                #Pauses Animation
                if(self.state == 'PAUSED'):
                    self.drawFrame = self.drawFrame
                    
                else:
                    self.drawFrame += 1
                
                    #Stops Animation
                    if self.drawFrame >= len(self.animation):
                        self.drawFrame = 0
                        self.state = 'STOP'
                        self.curFrame = self.stopFrame
                    
                    #Plays Animation
                    else:
                        self.curFrame = self.animation[self.drawFrame]
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
    
    spriteObj = SpriteLoader()
    spriteObj.loadMultiFile('assets/cow/')
    #spriteObj.loadSpriteSheet("assets/COWABUNGA.bmp", [0,0], [96,96], 1, 1)
    
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
                    if (spriteObj.state == 'STOP'):
                        spriteObj.state = 'PLAY'
                        print spriteObj.state
                    elif (spriteObj.state == 'PLAY'):    
                        spriteObj.state = 'PAUSED'
                        print spriteObj.state
                    elif (spriteObj.state == 'PAUSED'):    
                        spriteObj.state = 'PLAY'    
                        print spriteObj.state
                        
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
        screen.blit(spriteObj.curFrame, (100,100))
        msElapsed = clock.tick(30)
        pygame.display.update() 
    
if __name__ == '__main__':
    main()
    