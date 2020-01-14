from math import *
from sprites import *
from globals import *
from pygame.locals import *
from weapon import *



class player():
    def __init__(self, xPos, yPos, xDir, yDir, xPlane, yPlane):
        self.xPos = xPos
        self.yPos = yPos
        self.xDir = xDir
        self.yDir = yDir
        self.xPlane = xPlane
        self.yPlane = yPlane

        self.movementSpeed = 0.15
        self.rotationSpeed = 0.01

        self.currentHealth  = 100
        self.maxHealth = 100

        self.alive = True
        self.weapon = pistol()
        return

    def update(self, keys, worldMap):
        if keys[K_LSHIFT]:
            self.movementSpeed = 0.15
        else:
            self.movementSpeed = 0.05

        if keys[K_w]:
            if not worldMap[int(self.yPos)][int(self.xPos + self.xDir * self.movementSpeed)]:
                self.xPos += self.xDir * self.movementSpeed
            if not worldMap[int(self.yPos + self.yDir * self.movementSpeed)][int(self.xPos)]:
                self.yPos += self.yDir * self.movementSpeed

        if keys[K_s]:
            if not worldMap[int(self.yPos)][int(self.xPos - self.xDir * self.movementSpeed)]:
                self.xPos -= self.xDir * self.movementSpeed
            if not worldMap[int(self.yPos - self.yDir * self.movementSpeed)][int(self.xPos)]:
                self.yPos -= self.yDir * self.movementSpeed

        if keys[K_d]:
            if not worldMap[int(self.yPos)][int(self.xPos + self.xPlane * self.movementSpeed)]:
                self.xPos += self.xPlane * self.movementSpeed
            if not worldMap[int(self.yPos + self.yPlane * self.movementSpeed)][int(self.xPos)]:
                self.yPos += self.yPlane * self.movementSpeed


        if keys[K_a]:
            if not worldMap[int(self.yPos)][int(self.xPos - self.xPlane * self.movementSpeed)]:
                self.xPos -= self.xPlane * self.movementSpeed
            if not worldMap[int(self.yPos - self.yPlane * self.movementSpeed)][int(self.xPos)]:
                self.yPos -= self.yPlane * self.movementSpeed

        if keys[K_j]:
            self.weapon.shoot(self.xPos, self.yPos, worldMap)

        if keys[K_k]:
            self.xPos = 10.06089
            self.yPos = 6.43012

        if keys[K_RIGHT]:
            self.xDirOld = self.xDir
            self.xDir = self.xDir * cos(-self.rotationSpeed) - self.yDir * sin(-self.rotationSpeed)
            self.yDir = self.xDirOld * sin(-self.rotationSpeed) + self.yDir * cos(-self.rotationSpeed)
            self.xPlaneOld = self.xPlane
            self.xPlane = self.xPlane * cos(-self.rotationSpeed) - self.yPlane * sin(-self.rotationSpeed)
            self.yPlane = self.xPlaneOld * sin(-self.rotationSpeed) + self.yPlane * cos(-self.rotationSpeed)

        if keys[K_LEFT]:
            self.xDirOld = self.xDir
            self.xDir = self.xDir * cos(self.rotationSpeed) - self.yDir * sin(self.rotationSpeed)
            self.yDir = self.xDirOld * sin(self.rotationSpeed) + self.yDir * cos(self.rotationSpeed)
            self.xPlaneOld = self.xPlane
            self.xPlane = self.xPlane * cos(self.rotationSpeed) - self.yPlane * sin(self.rotationSpeed)
            self.yPlane = self.xPlaneOld * sin(self.rotationSpeed) + self.yPlane * cos(self.rotationSpeed)

        if pygame.mouse.get_pressed()[0]:
            self.weapon.shoot(self.xPos, self.yPos, worldMap)


        self.mouse = pygame.mouse.get_rel()
        self.xMouse = self.mouse[0]/100

        if self.xMouse < 0:
            self.xDirOld = self.xDir
            self.xDir = self.xDir * cos(-self.xMouse) - self.yDir * sin(-self.xMouse)
            self.yDir = self.xDirOld * sin(-self.xMouse) + self.yDir * cos(-self.xMouse)
            self.xPlaneOld = self.xPlane
            self.xPlane = self.xPlane * cos(-self.xMouse) - self.yPlane * sin(-self.xMouse)
            self.yPlane = self.xPlaneOld * sin(-self.xMouse) + self.yPlane * cos(-self.xMouse)

        if self.xMouse > 0:
            self.xDirOld = self.xDir
            self.xDir = self.xDir * cos(-self.xMouse) - self.yDir * sin(-self.xMouse)
            self.yDir = self.xDirOld * sin(-self.xMouse) + self.yDir * cos(-self.xMouse)
            self.xPlaneOld = self.xPlane
            self.xPlane = self.xPlane * cos(-self.xMouse) - self.yPlane * sin(-self.xMouse)
            self.yPlane = self.xPlaneOld * sin(-self.xMouse) + self.yPlane * cos(-self.xMouse)


        #End Controls

        self.healthBar = pygame.Rect(262, 100, (self.currentHealth/self.maxHealth)*500, 10)
        self.healthBarBackground = pygame.Rect(262, 100, 1*500, 10)
        if self.currentHealth < 1:
            self.alive = False
        pygame.draw.rect(screen, [169,169,169], self.healthBarBackground)
        pygame.draw.rect(screen, [255,0,0], self.healthBar)
        return



    def render(self, column, worldMap):
        self.xCamera = 2 * column / float(WIDTH) - 1.0
        self.xRayDir = self.xDir + self.xPlane * self.xCamera
        self.yRayDir = self.yDir + self.yPlane * self.xCamera

        self.xMap = int(self.xPos)
        self.yMap = int(self.yPos)

        self.xSideDistance = 0.0
        self.ySideDistance = 0.0
        self.perpWallDistance = 0.0

        self.xDeltaDistance = abs(1/(self.xRayDir + zde))
        self.yDeltaDistance = abs(1/(self.yRayDir + zde))

        self.xStep = 0
        self.yStep = 0

        self.side = 0

        if (self.xRayDir < 0):
            self.xStep = -1
            self.xSideDistance = (self.xPos - self.xMap) * self.xDeltaDistance
        else:
            self.xStep = 1
            self.xSideDistance = (self.xMap + 1.0 - self.xPos) * self.xDeltaDistance

        if (self.yRayDir < 0):
            self.yStep = -1
            self.ySideDistance = (self.yPos - self.yMap) * self.yDeltaDistance
        else:
            self.yStep = 1
            self.ySideDistance = (self.yMap + 1.0 - self.yPos) * self.yDeltaDistance


        self.hit = False

        while not self.hit:
            if (self.xSideDistance < self.ySideDistance):
              self.xSideDistance += self.xDeltaDistance
              self.xMap += self.xStep
              self.side = 'x'

            else:
              self.ySideDistance += self.yDeltaDistance
              self.yMap += self.yStep
              self.side = 'y'

            if worldMap[self.yMap][self.xMap] != 0 :
                self.hit = True


        if (self.side == 'x'):
            self.perpWallDist = (self.xMap - self.xPos + (1 - self.xStep) / 2) / (self.xRayDir + zde)
        else:
            self.perpWallDist = (self.yMap - self.yPos + (1 - self.yStep) / 2) / (self.yRayDir + zde)


        self.lineHeight = int(HEIGHT / (self.perpWallDist + zde))

        self.drawStart = -self.lineHeight / 2 + HEIGHT / 2

        if (self.drawStart < 0):
            self.drawStart = 0

        self.drawEnd = self.lineHeight / 2 + HEIGHT / 2

        if (self.drawEnd >= HEIGHT):
            self.drawEnd = HEIGHT - 1

        self.wallcolours = [[255,255,255], [150,0,0], [0,150,0], [0,0,150], [150,150,0]]
        self.sprite = ()
        if worldMap[self.yMap][self.xMap] <= 4:
            self.colour = self.wallcolours[worldMap[self.yMap][self.xMap]]

        elif worldMap[self.yMap][self.xMap] > 4:
            self.spriteID = worldMap[self.yMap][self.xMap]
            worldMap[self.yMap][self.xMap] = 0
            self.sprite = (self.xMap, self.yMap, self.spriteID)

            pass

        else:
            self.colour = None
            worldMap[self.yMap][self.xMap] = 0


        if self.colour != None:
            if self.side == 'y':
                self.colour = [i/2 for i in self.colour]

        return (self.colour, self.drawStart, self.drawEnd, self.perpWallDist, self.sprite)
