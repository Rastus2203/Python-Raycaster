import random
import pygame
from sprites import *
from player import *
from globals import *
from bisect import bisect_left
from mapGen import *
from math import *
from pygame.locals import *


spriteDict = {
    5: lukeHead,
    9: rifleItem

}

keys = [False]*324 #List for keyboard values
#zde = 0.0000001 #append to prvent division by zero
res = 2


#Creates the Map
#worldMap = mapGenBlank(20)
worldMap = mapGenTiled(5)

'''
worldMap[10][12] = 3
worldMap[11][12] = 3
worldMap[9][12] = 3
worldMap[9][11] = 3
worldMap[11][11] = 3
worldMap[15][10] = 4
#worldMap[5][10] = 4
'''


#enemies.append(enemy(screen, 5, 10, pink, worldMap))



for i in worldMap:
    print(''.join(str(i)))

rotationSpeed = 0.01
movementSpeed = 0.05

#Exits pygame
def close():
    pygame.display.quit()
    pygame.quit()
    quit()

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

clock = pygame.time.Clock()

player = player(10.0, 5.0, -0.7, 0, 0, 0.7)





#Start game loop
while player.alive:
    #Draws background. Black and Grey
    screen.fill((25,25,25))
    pygame.draw.rect(screen, (50,50,50), (0, HEIGHT/2, WIDTH, HEIGHT/2)) #Draws grey rectang sle in bottom half

    #Sets whether keys are held or not
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            keys[event.key] = True
        elif event.type == KEYUP:
            keys[event.key] = False



    #Keybindings
    if keys[K_ESCAPE]:
        close()

    player.update(keys, worldMap)

    for i in enemies:
        i.update(player)

    for i in items:
        i.update(player)



    angles = []
    drawBuffer = []
    for column in range(0, WIDTH, res):
        ray = player.render(column, worldMap)
        drawBuffer.append(('l', ray[0], column, ray[1], ray[2], ray[3]))
        if len(ray[4]) > 0:
            if ray[4][2] > 8:
                items.append(spriteDict[ray[4][2]](screen, ray[4][0], ray[4][1], worldMap))
            else:
                enemies.append(spriteDict[ray[4][2]](screen, ray[4][0], ray[4][1], worldMap))


    #a1 and a2 represent the angle of the first and last ray on the screen.
    #Calculated with the inverse tan of the player position and using the plane vector
    #180 was appended so that it returns values between 0 and 360, making it easier to deal with.
    a1 = degrees(atan2(((player.yPos + player.yDir - player.yPlane) - player.yPos), ((player.xPos + player.xDir - player.xPlane) - player.xPos)))+180
    a2 = degrees(atan2(((player.yPos + player.yDir + player.yPlane) - player.yPos), ((player.xPos + player.xDir + player.xPlane) - player.xPos)))+180


    #Deals with wrapping angles around cleanly so the difference between a1 and a2 is consistent.
    #appendAngle is a flag to let the enemy rendering code know that the angle has been wrapped

    #if a1 < a2:
    #    a1 += 360
    #    appendAngle = True
    #enemies = [x for x in enemies if x.currentHealth > 0]

    for i in enemies:
        if i.currentHealth < 0:
            enemies.remove(i)

    for i in items:
        if i.grabbed:
            items.remove(i)


    appendAngle = False
    for i in enemies:
        #appendAngle = False
        if a1 < a2:
            a1 += 360
            appendAngle = True

        #Returns a list of evenly spaced values between the two angles
        #angles = [a1 + x*(a2-a1)/(WIDTH/res) for x in range(int(WIDTH/res))]
        angles = [a1-x for x in baseAngles]

        #drawText(a1, 30, [0,255,0], (100,200))
        #drawText(a2, 30, [0,255,0], (100, 300))
        #drawText(i.angle, 30, [0,255,0], (500, 200))

        currentEnemy = i.render(player, angles, appendAngle, a1, a2, screen)
        if currentEnemy != None:
            drawBuffer += currentEnemy

    appendAngle = False
    for i in items:
        #appendAngle = False
        if a1 < a2:
            a1 += 360
            appendAngle = True

        #Returns a list of evenly spaced values between the two angles
        #angles = [a1 + x*(a2-a1)/(WIDTH/res) for x in range(int(WIDTH/res))]
        angles = [a1-x for x in baseAngles]

        #drawText(a1, 30, [0,255,0], (100,200))
        #drawText(a2, 30, [0,255,0], (100, 300))
        #drawText(i.angle, 30, [0,255,0], (500, 200))

        currentItem = i.render(player, angles, appendAngle, a1, a2, screen)
        if currentItem != None:
            drawBuffer += currentItem

    #Sorts the drawBuffer based on distance so that further objects are drawn first
    #This means that they will be drawn over if they are behind something
    drawBuffer.sort(key = lambda x: x[-1])
    for i in drawBuffer[::-1]:
        #If its a wall
        if i[0] == 'l':
            pygame.draw.line(screen, i[1], (i[2], i[3]), (i[2], i[4]), res)

        #If its a sprite
        elif i[0] == 's':
            screen.blit(i[1], i[2])

    player.weapon.render()

    #pygame.draw.line(screen, [255,0,0], (WIDTH/2, 0), (WIDTH/2, 1000))
    clock.tick(60)

    #drawText(clock.get_fps(), 30, [0,255,0], (100,300))

    pygame.display.update() #Updates screen
