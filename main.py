import pygame
import random
import math
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("background.png")
mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")

icon = pygame.image.load("rocket.png")

pygame.display.set_icon(icon)

playerimg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num = 6
for i in range(num):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
g_score = 0
font = pygame.font.Font("freesansbold.ttf",32)

textX= 10
testY= 10

over=pygame.font.Font("freesansbold.ttf",64)


def showscore(x,y):
    score=font.render("score:"+str(g_score),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over():
    over_text=over.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def player(x, y):
    screen.blit(playerimg, (playerX, playerY))


def enemy(x, y):
    screen.blit(enemyimg[i], (enemyX[i], enemyY[i]))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def Collision(enemyX, enemyY, bulletx, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bs=mixer.Sound("laser.wav")
                    bs.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking for the boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    for i in range(num):

        if enemyY[i] > 440:
            for j in range(num):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        coll = Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if coll:
            es = mixer.Sound("explosion.wav")
            es.play()
            bulletY = 480
            bullet_state = "ready"
            g_score += 1
            #print(g_score)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i])



    player(playerX, playerY)
    showscore(textX,testY)
    pygame.display.update()
