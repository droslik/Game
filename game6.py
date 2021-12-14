import pygame
import datetime
now = datetime.datetime.now()
pygame.init()
win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Hero and Enemies")

walkRight = [pygame.image.load('right_1.png'),
pygame.image.load('right_2.png'), pygame.image.load('right_3.png'),
pygame.image.load('right_4.png'), pygame.image.load('right_5.png'),
pygame.image.load('right_6.png'), pygame.image.load('right_7.png'),
pygame.image.load('right_8.png')]

walkLeft = [pygame.image.load('left_1.png'),
pygame.image.load('left_2.png'), pygame.image.load('left_3.png'),
pygame.image.load('left_4.png'), pygame.image.load('left_5.png'),
pygame.image.load('left_6.png'), pygame.image.load('left_7.png'),
pygame.image.load('left_8.png')]

jumpRight = [pygame.image.load('jump_right_1.png'),
pygame.image.load('jump_right_2.png')]

jumpLeft = [pygame.image.load('jump_left_1.png'),
pygame.image.load('jump_left_2.png')]

bg = pygame.image.load('bg.jpg')
playerStandright = pygame.image.load('stand_right.png')
playerStandleft = pygame.image.load('stand_left.png')



clock = pygame.time.Clock()

score = 0

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 6
        self.isJump = False
        self.jumpCount = 11
        self.left = False
        self.right = False
        self.animCount = 0
        self.lastMove = "right"
        self.hitbox = (self.x+40, self.y, self.width+40, self.height+118)

    def draw(self, win):

        if self.animCount + 1 >= 32:
            self.animCount = 0

        if self.left and not(self.isJump):
            win.blit(walkLeft[self.animCount // 4], (self.x, self.y))
            self.animCount += 1
        elif self.right and not(self.isJump):
            win.blit(walkRight[self.animCount // 4], (self.x, self.y))
            self.animCount += 1
        else:
            if self.lastMove == 'right' and not(self.isJump): #
                win.blit(playerStandright, (self.x, self.y))
            else:
                if self.lastMove == 'left' and not(self.isJump): #
                    win.blit(playerStandleft, (self.x, self.y))
        if self.isJump and self.lastMove == 'right':      #
            win.blit(jumpRight[self.jumpCount // 16], (self.x, self.y))    #

        if self.isJump and self.lastMove == 'left':       #
            win.blit(jumpLeft[self.jumpCount // 16], (self.x, self.y)) #
        self.hitbox = (self.x+40, self.y, self.width+40, self.height+118)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)    #2 - border
        for bullet in bullets:
            bullet.draw(win)


class enemy(object):
    walkRight1 = [pygame.image.load('enemy_right_1.png'),
    pygame.image.load('enemy_right_2.png'), pygame.image.load('enemy_right_3.png'),
    pygame.image.load('enemy_right_4.png')]

    walkLeft1 = [pygame.image.load('enemy_left_1.png'),
    pygame.image.load('enemy_left_2.png'), pygame.image.load('enemy_left_3.png'),
    pygame.image.load('enemy_left_4.png')]

    die_left = [pygame.image.load('enemy_die_left_1.png'),
    pygame.image.load('enemy_die_left_2.png'), pygame.image.load('enemy_die_left_3.png'),
    pygame.image.load('enemy_die_left_4.png'), pygame.image.load('enemy_die_left_5.png'),
    pygame.image.load('enemy_die_left_6.png'), pygame.image.load('enemy_die_empty.png'),
    pygame.image.load('enemy_die_left_6.png'), pygame.image.load('enemy_die_empty.png'),
    pygame.image.load('enemy_die_left_6.png'), pygame.image.load('enemy_die_empty.png')]
    die_right = [pygame.image.load('enemy_die_right_1.png'),
    pygame.image.load('enemy_die_right_2.png'), pygame.image.load('enemy_die_right_3.png'),
    pygame.image.load('enemy_die_right_4.png'), pygame.image.load('enemy_die_right_5.png'),
    pygame.image.load('enemy_die_right_6.png'), pygame.image.load('enemy_die_empty.png'),
    pygame.image.load('enemy_die_right_6.png'), pygame.image.load('enemy_die_empty.png'),
    pygame.image.load('enemy_die_right_6.png'), pygame.image.load('enemy_die_empty.png')]


    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        self.end = end
        self.path = [0, self.end]
        self.walkCount1 = 0
        self.vel = 3
        self.hitbox = (self.x, self.y, 100, 100)
        self.health = 9
        self.visible = True
        self.dieCount = 0

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount1 + 1 >= 32:
                self.walkCount1 = 0

            if self.vel > 0:
                win.blit(self.walkRight1[self.walkCount1 // 8], (self.x, self.y))
                self.walkCount1 += 1
            else:
                win.blit(self.walkLeft1[self.walkCount1 // 8], (self.x, self.y))
                self.walkCount1 += 1

        #drawing borders of health-indicator
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5*(9-self.health)), 10))
            self.hitbox = (self.x, self.y, 100, 100)
#drawing enemies death
        else:
            if facing == 1:
                if self.health == 0 and self.dieCount < 80:
                    win.blit(self.die_left[self.dieCount // 8], (self.x, self.y))
                    self.dieCount += 1
            else:
                if self.health == 0 and self.dieCount < 80:
                    win.blit(self.die_right[self.dieCount // 8], (self.x, self.y))
                    self.dieCount += 1

        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)  #if it is needed to see frame of enemy

#method for enemies movies
    def move(self):
        if self.visible:
            if self.vel > 0:
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount1 = 0
            else:
                if self.x - self.vel > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount1 = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
            enemies.append(fatman)
        print('hit')

#create class weapon
class weapon():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8*facing


    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def drawWindow():   #drawing of all elements

    win.blit(bg, (0, 0))        #fills background with the image
    text = font.render('Score: ' + str(score), 2, (0,0,0))
    win.blit(text, (10, 10))
    hero.draw(win)
    draw_victory()
    number_of_enemies = 0

    #several enemies
    for enemy in enemies:
        if number_of_enemies == 0:
            enemy.draw(win)
            number_of_enemies = 1
            if enemy.visible == False:
                number_of_enemies = 0
            if enemy.visible == False and enemy.health == 0:
                if score >= 40:
                    break
    pygame.display.update()

#function for drawing congrats
def draw_victory():
    congratsCount = 0
    congrats = [pygame.image.load('Congratulations.png'),
    pygame.image.load('congratulations_empty.png'), pygame.image.load('Congratulations.png'),
    pygame.image.load('congratulations_empty.png'),pygame.image.load('Congratulations.png'),
    pygame.image.load('congratulations_empty.png'),pygame.image.load('Congratulations.png'),
    pygame.image.load('congratulations_empty.png')]
    #text = font.render('Congratulations!', 4, (220,240,50))
    if score == 40:
        win.blit(congrats[congratsCount//32], (0, 42))
        congratsCount += 1
        #win.blit(text, (150, 250))

#mainloop
font = pygame.font.SysFont('calibri', 30, True)
run = True
hero = Player(50, 350, 35, 32)
shootLoop = 0
bullets = []    #empty list for bullets
# create enemies
fatman = enemy(-200, 395, 400)
fatman1 = enemy(700, 395, 400)
fatman2 = enemy(700, 395, 400)
fatman3 = enemy(-200, 395, 400)
fatman4 = enemy(700, 395, 400)
fatman5 = enemy(-200, 395, 400)
enemies = [fatman, fatman1, fatman2, fatman3, fatman4, fatman5]

while run:
    #goblin = enemy(0, 390, 400)
    clock.tick(35)
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        for enemy in enemies:  #my
            if enemy.visible == True:
                if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
                    if bullet.x-30 + bullet.radius > enemy.hitbox[0] and bullet.x+30 - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                        enemy.hit()
                        score += 1
                        bullets.pop(bullets.index(bullet))

        #flight of bullets in visible zone
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

#actions by pressing the buttons
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f] and shootLoop == 0:
        if hero.lastMove == 'right':
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5:
            bullets.append(weapon(round(hero.x + 75 ), round(hero.y + 60), 4, (255, 0, 0), facing))
        shootLoop = 1
    if keys[pygame.K_LEFT] and hero.x  > -40:  #x>40 - limitation of movement from the left side
        hero.x -= hero.speed
        hero.left = True
        hero.right = False
        hero.lastMove = 'left'
    elif keys[pygame.K_RIGHT] and hero.x < 500 - hero.width - 90:
        hero.x += hero.speed
        hero.left = False
        hero.right = True
        hero.lastMove = 'right'
    else:
        hero.left = False
        hero.right = False
        hero.animCount = 0
    if not(hero.isJump):
        if keys[pygame.K_SPACE]:    #jumping of the hero
            hero.isJump = True
    else:
        if hero.jumpCount >= -11:
            if hero.jumpCount < 0:
                hero.y += (hero.jumpCount ** 2) / 2
            else:
                hero.y -= (hero.jumpCount ** 2) / 2
            hero.jumpCount -= 1
        else:
            hero.isJump = False
            hero.jumpCount = 11
    drawWindow()

pygame.quit()
