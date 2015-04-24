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
 - set animation range through a start frame and end frame
 - specify a current animation frame
 - return which animation frame the animation is currently in
 - helper functions as needed
Rotate sprite
Scale sprite
 - Should be able to scale up and down
Get Width and Height (remember scaling)

#Advanced (A level specifications):

 - Fix the surface scaling problem with the Rotate command
 - Allow the user to create specific animations that are easily loaded 
 - Manipulate alpha to make sprite partially transparent
 - Debug mode that shows borders and animation frames
'''
import pygame, sys, os
from glob import *
 
class SpriteLoader(pygame.sprite.Sprite):
    
    def __init__(self):
        """Constructor"""
        pygame.sprite.Sprite.__init__(self)
        self.width = 0
        self.height = 0
        self.scale = 1
        self.animation = []
    
    def loadMultiFile(self, dirName):
        """Load from multiple graphic files"""
        
        dirScan = glob(dirName)
        fileCount = 0
        print(fileCount, len(dirScan))
        while(fileCount < len(dirScan)):
            print (fileCount)
            fileCount += 1
        '''
        while(fileCount < len(dirScan)):
            
        self.stopFrame = pygame.image.load("cowImages/stopped0002.bmp")
        self.stopFrame = self.stopFrame.convert()
        transColor = self.stopFrame.get_at((1, 1))
        self.stopFrame.set_colorkey(transColor)
        
        for i in range(10):
            imgName = "cowImages/muuuh e000%d.bmp" % i
            tmpImage = pygame.image.load(imgName)
            tmpImage = tmpImage.convert()
            transColor = tmpImage.get_at((1, 1))
            tmpImage.set_colorkey(transColor)
            self.animation.append(tmpImage)
        '''
        
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
    
    def animate(self):
        '''
        - play/pause animation
        - change animation delay
        - set animation range through a start frame and end frame
        - specify a current animation frame
        - return which animation frame the animation is currently in
        - helper functions as needed
        '''
        pass
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
    
    def scale(self):
        #Should be able to scale up and down
        pass
    
    def getWidth(self):
        return self.width*self.scale
    
    def getHeight(self):
        return self.height*self.scale

def main():
    spriteObj = SpriteLoader()
    spriteObj.loadMultiFile('assets/cow/*.*')
    print ("Executed")
    
if __name__ == '__main__':
    main()
    