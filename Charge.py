import pygame,random,time
pygame.init()

#COLORS
Blue=(0,102,204)
lBlue=(102,178,255)
dBlue=(0,0,153)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
yellow=(255,255,0)
cyan=(0,255,255)
gray=(128,128,128)
white=(255,255,255)
purple=(255,0,255)

#SPRITES
PlayerSprite=pygame.image.load('sprites/PlayerSprite.png')

Lime=pygame.image.load('sprites/LimeEnemy.png')
White=pygame.image.load('sprites/WhiteEnemy.png')
Purple=pygame.image.load('sprites/PurpleEnemy.png')
Yellow=pygame.image.load('sprites/YellowEnemy.png')
Grey=pygame.image.load('sprites/GreyEnemy.png')
Red=pygame.image.load('sprites/RedEnemy.png')
Brown=pygame.image.load('sprites/BrownEnemy.png')
Orange=pygame.image.load('sprites/OrangeEnemy.png')
Blue=pygame.image.load('sprites/BlueEnemy.png')

splash=pygame.image.load('sprites/splash.png')
bg=pygame.image.load('sprites/BlueGuy.png')
GameOver=pygame.image.load('sprites/Game Over.png')
end=pygame.image.load('sprites/black.png')

#VARIABLES
wLen=700
wHeight=500

Lwall=20
Rwall=wLen-20
top=47
floor=wHeight-20

eSpawn=580
eSpawnY=floor-64

score=0
stopwatch=60.0
init=stopwatch
blockFont=pygame.font.SysFont('block',40,False)

bullets=[]
Ebullets=[]
bNum=1
shootLoop=0

shoot=pygame.mixer.Sound('sounds/bullet.wav')
gameOver=pygame.mixer.Sound('sounds/gameOver.wav')
introMus=pygame.mixer.Sound('sounds/intro.wav')

fallBack=0

clock=pygame.time.Clock()
keys=pygame.key.get_pressed()

global run
run=True

pq=False

lose=False

global level
level=1

moveX=True
moveY=True


#WINDOWS
win=pygame.display.set_mode((wLen,wHeight))
pygame.display.set_caption('Charge!!!')

lostWin=pygame.display.set_mode((wLen,wHeight))

#CLASSES
class player(object):
    def __init__(self,x,y,w,h,v,c):
        self.x =x
        self.y =y
        self.w =w
        self.h =h
        self.v =v
        self.c =c
        
    def draw(self,win):
        win.blit(PlayerSprite,(self.x,self.y))


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x =x
        self.y =y
        self.radius =radius
        self.color =color
        self.facing =facing
        self.vel =16*facing

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)


class enemy(object):
    def __init__(self,y,v,health,wavy,sprite):
        self.x =580
        self.y =y
        self.w =20
        self.h =50
        self.v =v
        self.health =health
        self.wavy =wavy
        self.sprite =sprite
        self.hitbox =(self.x+5,self.y+10,self.w,self.h)

    def move(self):
        if self.x != 20:
            if self.wavy==False:
                self.x-=self.v
            elif self.wavy==True:

                #LEFT
                self.x-=self.v
                self.x-=self.v

                #UP/DOWN
                self.y-=self.v
                self.y-=self.v
                self.y+=self.v
                
            else:
                run=False

    def draw(self):
        self.move()
        win.blit(self.sprite,(self.x,self.y))
        self.hitbox=(self.x+10,self.y+20,self.w,self.h)
        #pygame.draw.rect(win,yellow,self.hitbox,1)

    def hit(self):
        global score
        score+=1
        if self.health>0:
            self.health-=1
           

#PLAYER AND NON-PLAYER CHARACTERS
guy=player(20,floor-64,55,63,10,Blue)


slowGuy=enemy(floor-64,4,10,False,Lime)
fastGuy=enemy(floor-104,9,5,False,White)
tiltGuy=enemy(floor-64,3,4,True,Purple)

quickGuy=enemy(floor-64,8,6,False,Blue)
ClothesMasher=enemy(floor-74,5,3,True,Grey)
trump=enemy(floor-69,3,12,True,Orange)

yellowGuy=enemy(floor-94,5,9,False,Yellow)
brownGuy=enemy(floor-64,6,10,False,Brown)
boss=enemy(floor-100,2,15,False,Red)


#FUNCTIONS
def wait(s=1):
    time.sleep(s)


def RGW():
    win.blit(bg,(0,0))
    pygame.draw.rect(win,dBlue,(0,floor,wLen,50))
    pygame.draw.rect(win,black,(0,0,wLen,42))

    guy.draw(win)
    #discord(guy)

    scoreText=blockFont.render("Score: "+str(score),1,white)
    win.blit(scoreText,(wLen-150,9))

    global stopwatch
    stopwatchText=blockFont.render("Time: "+str(stopwatch),1,white)
    win.blit(stopwatchText, (20,9))
    stopwatch-=0.1
    
    if level==1:
        slowGuy.draw()
        #discord(slowGuy)
    if level==2:
        fastGuy.draw()
        #discord(fastGuy)
    if level==3:
        tiltGuy.draw()
        #discord(tiltGuy)
    if level==4:
        quickGuy.draw()
        #discord(quickGuy)
    if level==5:
        ClothesMasher.draw()
        #discord(ClothesMasher)
    if level==6:
        trump.draw()
        #discord(trump)
    if level==7:
        yellowGuy.draw()
        #discord(yellowGuy)
    if level==8:
        brownGuy.draw()
        #discord(brownGuy)
    if level==9:
        boss.draw()
        #discord(boss)


    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

    if lose==True:
        x=0
        while x==0:
            pygame.display.set_caption('YOU LOSE')
            win.blit(GameOver,(0,0))
            pygame.display.update()
            gameOver.play()
            wait(3)
            x+=1


def discord(thing):
    print(thing.x,thing.y)


def SHOOT():
    shoot.play()


def collision(enemy):
    if bullet.y-bullet.radius<enemy.hitbox[1]+enemy.hitbox[3] and bullet.y+bullet.radius>enemy.hitbox[1]:
        if bullet.x+bullet.radius>enemy.hitbox[0] and bullet.x-bullet.radius<enemy.hitbox[0]+enemy.hitbox[2]:
            enemy.hit()
            if bullet not in bullets:
                fallBack=0
            else:
                bullets.pop(bullets.index(bullet))

            if enemy.health==0:
                enemy.x=-100
                enemy.v=0


def winCheck(enemy,lvl,final=False):
    global level
    if enemy.health==0 and level==lvl:
        level+=1
        if final==True:
            global run
            print('GREAT JOB!!')
            wait()
            run=False


def loseCheck(enemy):
    if enemy.x<=20 and enemy.x!=-100:
        global lose
        lose=True
        run=False


#SPLASH SCREEN
intro=True

while intro:
    win.blit(splash,(0,0))
    pygame.display.update()
    introMus.play()
    wait(2.5)
    break

    #X BUTTON
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            intro=False
            run=False
            pq=True


#MAINLOOP
while run and stopwatch>0:
    clock.tick(30)
    pygame.time.delay(100)


    #X BUTTON
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False


    #LOSS CONDITIONS
    loseCheck(slowGuy)
    loseCheck(fastGuy)
    loseCheck(tiltGuy)
    loseCheck(quickGuy)
    loseCheck(ClothesMasher)
    loseCheck(trump)
    loseCheck(yellowGuy)
    loseCheck(brownGuy)
    loseCheck(boss)
    
    if stopwatch==0:
        lose()
        run=False
        

    #WIN CONDITIONS
    winCheck(slowGuy,1)
    winCheck(fastGuy,2)
    winCheck(tiltGuy,3)
    winCheck(quickGuy,4)
    winCheck(ClothesMasher,5)
    winCheck(trump,6)
    winCheck(yellowGuy,7)
    winCheck(brownGuy,8)
    winCheck(boss,9,True)


    #SHOOT DELAY
    if shootLoop>0:
        shootLoop+=1
    if shootLoop>6:
        shootLoop=0


    #BULLET MECHANICS
    for bullet in bullets:
        #COLLISION
        collision(fastGuy)
        collision(slowGuy)
        collision(tiltGuy)
        collision(quickGuy)
        collision(ClothesMasher)
        collision(trump)
        collision(yellowGuy)
        collision(brownGuy)
        collision(boss)
        

        if bullet.x<wLen and bullet.x>0:
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))    
    keys=pygame.key.get_pressed()

    if moveX==True:
        #MOVE LEFT
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and guy.x>Lwall:
            guy.x-=guy.v

        #MOVE RIGHT
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and guy.x<Rwall-guy.w:
            guy.x+=guy.v

    if moveY==True:
        #MOVE UP
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and guy.y>17:
            guy.y-=guy.v
            
        #MOVE DOWN
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and guy.y<floor-64:
            guy.y+=guy.v

    #SHOOT
    if keys[pygame.K_SPACE] and shootLoop==0:
        facing=1    
        SHOOT()
        bullets.append(projectile(round(guy.x+guy.w+10), round(guy.y+guy.h-27), 6, gray, facing))
        guy.draw(win)
        shootLoop=1

    #FORCE QUIT
    if keys[pygame.K_q]:
        run=False

    RGW()
    if lose==True:
        run=False


b=0
introMus.play()
while b!=5 and lose==False and pq==False:
    win.blit(end,(0,0))
    scoreText=blockFont.render("Score: "+str(score),1,white)
    win.blit(scoreText,(wLen/3,wHeight/2))

    stopwatchText=blockFont.render("Time: "+str(stopwatch),1,white)
    win.blit(stopwatchText, (wLen/3,wHeight/2+50))
    
    pygame.display.update()
    wait()
    b+=1

pygame.quit()

