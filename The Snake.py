import pygame,time,sys,random
from pygame import mixer
pygame.init()



speed = 20
white = pygame.Color(255, 255, 255)   
bg = pygame.image.load("space.jpg")
apple = pygame.image.load("apple.png")
skin = pygame.image.load("snake.png")
menubg = pygame.image.load("menu.jpg")
mixer.music.load("cute.mp3")
mixer.music.play(-1)

class Snake(object):
    def __init__(self):
        self.Spos = [100,50]
        self.body = [[100,50],[90,50],[80,50]]
        self.direction = "RIGHT"
        self.vel = 10

    def DirectionCheck(self,dirchange):
        if dirchange == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'
        if dirchange == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        if dirchange == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        if dirchange == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'

    def Movement(self,foods):
        if self.direction == 'RIGHT':
            self.Spos[0] += self.vel
        if self.direction == 'LEFT':
            self.Spos[0] -= self.vel
        if self.direction == 'UP':
            self.Spos[1] -= self.vel
        if self.direction == 'DOWN':
            self.Spos[1] += self.vel
        self.body.insert(0,list(self.Spos))
         
        if self.Spos == foods:
            return 1
        else:
            self.body.pop()
            return 0
        

    def Collision(self):
        if self.Spos[0] > 710 or self.Spos[0] < 0:
           return 1
        if self.Spos[1] > 450 or self.Spos[1] < 0:
           return 1
        for block in self.body[1:]:
            if self.Spos[0] == block[0] and self.Spos[1] == block[1]:
                return 1

 
class Food(object):
    def __init__(self):
        self.FPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
        self.FIn = True

    def FoodSpawn(self):
       if self.FIn == False:
           self.FPos  = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
           self.FIn = True
       return self.FPos

    def setFood(self,x):
        self.FIn = x
    
PlaySurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('The Snake')
FPS = pygame.time.Clock()

score = 0

Player = Snake()
Snack = Food()

def gameOver():
    mixer.music.load("gameover.wav")
    mixer.music.play()
    gFont = pygame.font.SysFont('comicsansms', 72)
    fFont = pygame.font.SysFont('comicsansms', 42)
    GOsurf = gFont.render("Final Score :"+ str(score), True, white)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360, 50)
    PlaySurface.blit(GOsurf,GOrect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    sys.exit()
    
menu = True
while True:
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    menu = False
                elif event.key == pygame.K_LEFT:
                    menu = False
                elif event.key == pygame.K_UP :
                    menu = False
                elif event.key == pygame.K_DOWN:
                    menu = False
                            
        PlaySurface.blit(menubg,(0,0))
        gFont = pygame.font.SysFont('comicsansms', 72)
        pause = gFont.render('The Snake', True, white)
        ppos = pause.get_rect()
        ppos.midtop = (360, 50)
        PlaySurface.blit(pause, ppos)
        hFont = pygame.font.SysFont('comicsansms', 42)
        pauses = hFont.render('Press Any Arrow Keys To Play', True, white)
        gpos = pauses.get_rect()
        gpos.midtop = (360, 250)
        PlaySurface.blit(pauses, gpos)
        pygame.display.flip()
        FPS.tick(30)
        pygame.display.update()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        pressed = pygame.key.get_pressed()
 
        if pressed[pygame.K_RIGHT]:
            Player.DirectionCheck('RIGHT')
        elif pressed[pygame.K_LEFT]:
            Player.DirectionCheck('LEFT')
        elif pressed[pygame.K_UP]:
            Player.DirectionCheck('UP')
        elif pressed[pygame.K_DOWN]:
            Player.DirectionCheck('DOWN')
        elif pressed[pygame.K_ESCAPE]:
            gameOver()

    PlaySurface.blit(bg,(0,0))
    foodie = Snack.FoodSpawn()
    if Player.Movement(foodie) == 1:
        effect = mixer.Sound('point.wav')
        effect.play()
        score += 1
        speed += 1
        Snack.setFood(False)

        
    for pos in Player.body:
        PlaySurface.blit(skin,pygame.Rect(pos[0], pos[1], 10, 10))
    PlaySurface.blit(apple,pygame.Rect(Snack.FPos[0], Snack.FPos[1], 10, 10))

    
    if(Player.Collision() == 1):
        gameOver()

    pygame.display.set_caption("The Snake | Score: " + str(score))
    pygame.display.flip()
    FPS.tick(speed)

            
