'''
#PygameSpriteClass
Ethan Richardson
'''

import pygame, sys
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
        
        self.speed = 0
        self.delay = 3
        
        self.beg = -1
        self.end = -1
        
        
    def loadMultiFile(self, dirName):
        """Load from Multiple Sprite Files"""
        self.stopFrame = pygame.image.load(dirName + "00.bmp").convert()
        
        dirScan = glob(dirName + "*.*")
        for i in range(1,len(dirScan)):
            self.animation.append(pygame.image.load(dirScan[i]).convert())
            
        self.width = self.stopFrame.get_width()
        self.height = self.stopFrame.get_height()   
           
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
        
        self.width = self.stopFrame.get_width()
        self.height = self.stopFrame.get_height()         
        
    def animate(self):
        """Loops Sprite Animation"""
        if self.state == 'STOP':
            self.curFrame = self.stopFrame
        else:
            #Defaults, setAnimationRange never called
            if(self.end == -1):
                self.end = len(self.animation)
            if(self.beg == -1):
                self.beg = 0
                
            self.speed += 1
            
            #Sets up Animation Speed
            if self.speed > self.delay:
                self.speed = 0
                
                #Plays/Pauses Animation
                if(self.state != 'PAUSED'):
                    self.beg += 1
                        
                    #Resets Animation
                    if self.beg >= self.end:
                        self.beg = -1
                        self.curFrame = self.stopFrame
                
                self.curFrame = self.animation[self.beg]

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
    
    def stopAnimation(self):
        """
        Sets State Flag to STOP
        Resets animation to 0-th frame
        """
        self.state = 'STOP'
        self.beg = -1
    
    def setAnimationDelay(self, delay):
        """
        Sets Animation Delay
        Default Delay: 3
        """
        self.delay = delay
    
    def setAnimationRange(self, beg, end):
        self.beg = beg
        self.end = end
        
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
    spriteObj.loadMultiFile('assets/cow/')

    #Uncomment for SpriteSheet file cow
    #spriteObj.loadSpriteSheet("assets/COWABUNGA.bmp", [0,0], [96,96], 12, 1)
    
    #Uncomment for Cow TransColor
    spriteObj.setTransColor((111, 79, 51, 255))    
    
    #Uncomment for SpriteSheet file asteroid
    #spriteObj.loadSpriteSheet("assets/asteroid.bmp", [0,0], [64,64], 8, 8)
    #spriteObj.setTransColor((255, 0, 255, 255))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    
    background.blit(background, (0, 0))
    
    #Uncomment for AnimationRange
    #spriteObj.setAnimationRange(2, 4)   
    
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
                if event.key == pygame.K_BACKSPACE:
                    spriteObj.stopAnimation()
                    print spriteObj.getState()
                        
        spriteObj.setAnimationDelay(3)      
        spriteObj.animate()
        
        screen.blit(spriteObj.curFrame, (100,100))
        msElapsed = clock.tick(30)
        pygame.display.update() 
    
if __name__ == '__main__':
    main()
    