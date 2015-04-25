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
    
    def __init__(self):
        """Constructor"""
        pygame.sprite.Sprite.__init__(self)
        self.width = 0
        self.height = 0
        self.resize = 1
        self.drawFrame = 0
        self.animation = []
        self.curFrame = 0
    
    def loadMultiFile(self, dirName):
        """Load from multiple graphic files"""
        #First frame will always be stopFrame
        self.stopFrame = pygame.image.load(dirName + "00.bmp")
        self.stopFrame = self.stopFrame.convert()
        #Put in Draw
        transColor = self.stopFrame.get_at((1, 1))
        self.stopFrame.set_colorkey(transColor)
        
        dirScan = glob(dirName + "*.*")
        
        for i in range(1,len(dirScan)):
            animFrame = dirScan[i]
            tempFrame = pygame.image.load(animFrame)
            tempFrame = tempFrame.convert()
            #Put in Draw
            transColor = tempFrame.get_at((1, 1))
            tempFrame.set_colorkey(transColor)
            self.animation.append(tempFrame)
            print(dirScan[i])
        
        
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
        self.drawFrame += 1
        if self.drawFrame >= len(self.animation):
            self.drawFrame = 0
        self.stopFrame = self.animation[self.drawFrame]
        '''
        - play/pause animation
        - change animation delay
        - set animation range through a start frame and end frame
        - specify a current animation frame
        - return which animation frame the animation is currently in
        - helper functions as needed
        '''
        
    
    def rotate(self, angle):
        self.stopFrame = pygame.transform.rotate(self.stopFrame, angle)
    
    #TODO: Make Dynamic
    def resizeSprite(self, objective):
        """Resizes Sprite"""
        if(objective == 'scale'):
            wid = self.stopFrame.get_width()*SCALING_FACTOR
            ht = self.stopFrame.get_width()*SCALING_FACTOR
        elif(objective == 'shrink'):
            wid = self.stopFrame.get_width()/SCALING_FACTOR
            ht = self.stopFrame.get_width()/SCALING_FACTOR
        
        self.stopFrame = pygame.transform.scale(self.stopFrame, (wid,ht))
    
    def getWidth(self):
        return self.width*self.resize
    
    def getHeight(self):
        return self.height*self.resize

def main():
    
    spriteObj = SpriteLoader()
    spriteObj.loadMultiFile('assets/cow/')
    
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    
    background.blit(background, (0, 0))
    
    while(True):
        screen.blit(background, (0, 0))
        #screen.fill(Color.black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spriteObj.animate()
                if event.key == pygame.K_UP:
                    spriteObj.resizeSprite('scale')
                if event.key == pygame.K_DOWN:
                    spriteObj.resizeSprite('shrink')
                if event.key == pygame.K_LEFT:
                    spriteObj.rotate(90)
                    print("rotate 90deg Left")
                if event.key == pygame.K_RIGHT:
                    spriteObj.rotate(-90)
                    print("rotate 90deg Right")
        
        screen.blit(spriteObj.stopFrame,(100,100))
        #spriteObj.animate
        msElapsed = clock.tick(30)
        pygame.display.update() 
    
if __name__ == '__main__':
    main()
    