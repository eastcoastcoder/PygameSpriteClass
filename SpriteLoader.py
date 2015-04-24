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
 
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
 
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
        #First frame will always be stopFrame
        self.stopFrame = pygame.image.load(dirName + "00.bmp")
        self.stopFrame = self.stopFrame.convert()
        #Put in Draw
        transColor = self.stopFrame.get_at((1, 1))
        self.stopFrame.set_colorkey(transColor)
        
        dirScan = glob(dirName + "*.*")
        
        for i in range(1,len(dirScan)):
            animFrame = dirScan[i]
            curFrame = pygame.image.load(animFrame)
            curFrame = curFrame.convert()
            #Put in Draw
            transColor = curFrame.get_at((1, 1))
            curFrame.set_colorkey(transColor)
            self.animation.append(curFrame)
            print(dirScan[i])
        
        '''
        
        for i in range(10):
            animFrame = "cowImages/muuuh e000%d.bmp" % i
            curFrame = pygame.image.load(animFrame)
            curFrame = curFrame.convert()
            transColor = curFrame.get_at((1, 1))
            curFrame.set_colorkey(transColor)
            self.animation.append(curFrame)
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
        self.stopFrame = pygame.transform.rotate(self.stopFrame, angle)
    
    def scale(self):
        #Should be able to scale up and down
        pass
    
    def getWidth(self):
        return self.width*self.scale
    
    def getHeight(self):
        return self.height*self.scale

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
                    pass
                if event.key == pygame.K_DOWN:
                    pass
                if event.key == pygame.K_LEFT:
                    spriteObj.rotate(90)
                    print("rotate 90deg Left")
                if event.key == pygame.K_RIGHT:
                    spriteObj.rotate(-90)
                    print("rotate 90deg Right")
        
        screen.blit(spriteObj.stopFrame,(100,100))
        msElapsed = clock.tick(30) #SYNC RATE 30 FPS
        pygame.display.update() #SYNC 
    
if __name__ == '__main__':
    main()
    