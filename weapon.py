import pygame
from pygame.locals import *
from globals import *

pistolSprite = pygame.image.load("pistol.png")
pistolSprite = pygame.transform.scale(pistolSprite, (234, 309))

pistolFireSprite = pygame.image.load("pistolFire.png")
pistolFireSprite = pygame.transform.scale(pistolFireSprite, (123, 114))

rifleSprite = pygame.image.load("rifle.png")
rifleSprite = pygame.transform.scale(rifleSprite, (249, 183))

rifleFireSprite = pygame.image.load("rifleFire.png")
rifleFireSprite = pygame.transform.scale(rifleFireSprite, (249, 234))

class weapon():
    def __init__(self):
        self.now = pygame.time.get_ticks()
        self.lastFire = 0

    def shoot(self, xPos, yPos, worldMap):
        self.now = pygame.time.get_ticks()
        if self.now - self.lastFire > self.fireDelay:
            self.lastFire = self.now
            for enemy in enemies:
                
                if lineOfSight((xPos, yPos), (enemy.x, enemy.y), worldMap):

                    #if enemy.lineX < 500:
                    if (enemy.column > WIDTH/2 - enemy.newSize[0]/2) and (enemy.column < WIDTH/2 + enemy.newSize[0]/2):
                        enemy.currentHealth -= self.baseDamage # self.baseDamage






class rifle(weapon):
    def __init__(self):
        super().__init__()

        self.baseDamage = 10
        self.fireDelay = 50
        self.fireLength = 25



    def render(self):
        self.xPos =  WIDTH/2 - rifleSprite.get_size()[0]/2
        self.yPos = HEIGHT - rifleSprite.get_size()[1]
        screen.blit(rifleSprite, (self.xPos, self.yPos) )
        self.now = pygame.time.get_ticks()
        if self.now - self.lastFire < self.fireLength:
            screen.blit(rifleFireSprite, (self.xPos, HEIGHT - rifleFireSprite.get_size()[1]))

class pistol(weapon):
    def __init__(self):
        super().__init__()

        self.baseDamage = 20
        self.fireDelay = 400
        self.fireLength = 200



    def render(self):
        self.xPos =  WIDTH/2 - pistolSprite.get_size()[0]/2 - 45
        self.yPos = HEIGHT - pistolSprite.get_size()[1]
        screen.blit(pistolSprite, (self.xPos, self.yPos) )
        self.now = pygame.time.get_ticks()
        if self.now - self.lastFire < self.fireLength:
            screen.blit(pistolFireSprite, (self.xPos+96, self.yPos - 18))
