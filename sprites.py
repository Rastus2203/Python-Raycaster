import pygame
from bisect import bisect_left
from math import *
from globals import *
from weapon import *

lukeHeadSprite = pygame.image.load("lukeHead.png")
rifleSprite = pygame.image.load("rifleSprite.png")
#rifleSprite = pygame.transform.scale(rifleSprite, (10,10))






HEIGHT = 768
WIDTH = 1024

#Base entity class that handles the drawing of selfs
class entity():

    def __init__(self, screen, x, y, image, worldMap):
        super().__init__()

        self.screen = screen
        self.image = image
        self.x = x
        self.y = y
        self.dist = 0
        self.angle = 0.0
        self.column = 0
        self.newSize = image.get_size()
        self.worldMap = worldMap
        self.path = ()
        self.lastX = x
        self.lastY = y
        self.repath = False
        self.posCheck = ()
        self.lineX = 0
        self.yScreen = 0

        return

    def render(self, player, angles, addAngle, a1, a2, screen):
        self.out = []
        #Angle of the entity.
        self.angle = degrees(atan2(self.y -(player.yPos + player.yDir), self.x - (player.xPos + player.xDir)))+180


        self.invDet = 1.0 / (player.xPlane * player.yDir - player.xDir * player.yPlane)
        self.transformX = self.invDet * (player.yDir * (self.x-player.xPos) - player.xDir * (self.y-player.yPos))
        self.transformY = self.invDet * (-player.yPlane * (self.x-player.xPos) + player.xPlane * (self.y-player.yPos))
        self.spriteScreenX = int((WIDTH / 2) * (1 + self.transformX / self.transformY))




        #Correction for when the angle wraps back to 0 from 360
        if self.angle < 90 and addAngle:
            self.angle += 360


        #If entity on screen
        if not (self.angle > a1 or self.angle < a2):
            #Pythagoras to find the distance
            self.dist = sqrt(abs((player.xPos-self.x)**2 + ((player.yPos-self.y)**2)))

            self.height = int(HEIGHT/(self.dist))

            #Resizes the image based on the distance
            self.newImage = pygame.transform.scale(self.image, [self.height, self.height])
            self.newSize = self.newImage.get_size()

            self.column = self.spriteScreenX - self.newSize[0]/2

            #Splits the image into vertical strips to be drawn individually
            #This allows images to be correctly draw when partly behind objects
            self.strips = []
            for i in range(0, self.newSize[0]):
                self.strips.append((self.newImage.subsurface(i, 0, 1, self.newSize[1]), i))


            for i in self.strips:
                self.lineX = (self.spriteScreenX - (self.newSize[0]) + i[1])
                self.yScreen = (HEIGHT - self.newImage.get_rect().size[1]) / 2



                self.out.append(('s', i[0], [self.lineX, self.yScreen], self.dist))
            #drawText(self.column*2 , 30, [0,255,100], (700,200))

        return self.out


class enemy(entity):
    def __init__(self, screen, x, y, image, worldMap):
        super().__init__(screen, x, y, image, worldMap)

        self.goal = []
        self.now = pygame.time.get_ticks()

        return

    def update(self, player):
        '''
        if self.pathFind(player):
            #print(player.currentHealth)
            player.currentHealth -= 10'''

        self.healthBar = pygame.Rect(self.lineX - self.newSize[0], self.yScreen - 100, self.newSize[0] * (self.currentHealth/self.maxHealth), 10)
        self.healthBarBackground = pygame.Rect(self.lineX - self.newSize[0], self.yScreen - 100, self.newSize[0], 10)
        pygame.draw.rect(screen, [169,169,169], self.healthBarBackground)
        pygame.draw.rect(screen, [255,0,0], self.healthBar)
        self.pathFind(player)

        return

    def move(self, p2):
        self.xDelta = p2[0] - self.x
        self.yDelta = p2[1] - self.y
        self.moveDist = sqrt((self.xDelta)**2 + (self.yDelta)**2)

        self.xRatio = self.xDelta / self.moveDist
        self.yRatio = self.yDelta / self.moveDist

        self.xDelta = self.movementSpeed * self.xRatio
        self.yDelta = self.movementSpeed * self.yRatio



        if self.dist > 2 or self.dist == 0:
            #if self.worldMap[int(self.y)][int(self.x+self.xDelta)] == 0:
            self.x += self.xDelta
            #if self.worldMap[int(self.y+self.yDelta)][int(self.x)] == 0:
            self.y += self.yDelta
            return False
        return True



    def moveSquare(self, p2):
        self.x = p2[0]
        self.y = p2[1]
        return



    def pathFind(self, player):

        if lineOfSight((player.xPos, player.yPos), (self.x, self.y), self.worldMap):
            self.lastX = self.x
            self.lastY = self.y
            if self.move((player.xPos, player.yPos)):
                print(player.xPos, player.yPos, self.x, self.y, self.dist)
                player.currentHealth -= self.damage

        else:
            if self.goal == [] or pygame.time.get_ticks() - self.now > 500:
                self.pathResult = bfs((self.x, self.y), (player.xPos, player.yPos), self.worldMap)
                if self.pathResult != None:
                    self.path = self.pathResult


            self.goal = self.path[-1]
            if (self.goal[0]-0.1 < self.x and self.goal[0] + 0.1 > self.x) or (self.goal[1]-0.1 < self.y and self.goal[1] + 0.1 > self.y) and len(self.path)>1:
                try:
                    self.goal = self.path[-2]
                except:
                    pass

            self.lastX = self.x
            self.lastY = self.y

            if self.move(self.goal):
                print(player.xPos, player.yPos, self.x, self.y, self.dist)
                player.currentHealth -= self.damage
            return

class lukeHead(enemy):
    def __init__(self, screen, x, y, worldMap):

        self.image = lukeHeadSprite
        super().__init__(screen, x, y, self.image, worldMap)
        self.currentHealth = 99
        self.maxHealth = 99
        self.movementSpeed = 0.05
        self.damage = 3
        return

#Will be useful later.
class item(entity):
    def __init__(self, screen, x, y, image, worldMap):
        super().__init__(screen, x, y, image, worldMap)
        self.grabbed = False
        return



class rifleItem(item):
    def __init__(self, screen, x, y, worldMap):
        self.image = rifleSprite
        super().__init__(screen, x, y, self.image, worldMap)
        return

    def update(self, player):
        if self.dist < 2:
            self.grabbed = True
            player.weapon = rifle()
            return
