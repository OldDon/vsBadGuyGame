import pygame, sys, random, time
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")
screen=pygame.display.set_mode((640,650))
badguy_image = pygame.image.load("images/badguy.png").convert()
badguy_image.set_colorkey((0,0,0))
fighter_image = pygame.image.load("images/fighter.png").convert()
fighter_image.set_colorkey((255,255,255))
missile_image = pygame.image.load("images/missile.png").convert()
missile_image.set_colorkey((255,255,255))
last_badguy_spawn_time = 0

score = 0 # Set score variable 
font = pygame.font.Font(None,20) # Set font variable to display score...Note syntax




class Badguy:

    def __init__(self, *args, **kwargs):
        self.x = random.randint(0,520)
        self.y = -100
        self.dy = random.randint(2,6)
        self.dx = random.choice((-1,1))*self.dy
        
        #self.x = 285   
        #self.y = -100
        #self.dy=0

    def move(self):
            self.x += self.dx
        #self.dy +=0.2
            self.y += self.dy

        # self.y +=5 # Bad Guy moves down surface by 5 every game loop
        # if self.y > 300:
            #if self.y > 150 and self.y < 250:
            #    self.x += 5
            #if self.y > 250:
            #    # self.x +=5 # Line only executes once Bad Guy has reached 300 px down the surface
            #    self.x -=5

    def bounce(self):
        if self.x <0 or self.x >570:
            self.dx *=-1

    def score(self):
        global score # global allows a variable to be changed from...
                     # outside the funtion or class it was created in
        score += 100                    
    


    def draw(self):
        screen.blit(badguy_image,(self.x,self.y))
        

    
    def off_bottom_screen(self): # Once a badguy makes it off the bottom of the screen, remove from list
        return self.y > 640 # This is testing for the bottom of the game window. 'screen' variable is set to 640, 650. See setup at top of file.

    def touching(self, missile):
        return (self.x+35-missile.x)**2+(self.y+22-missile.y)**2<1225

class Fighter:
    def __init__(self):
        self.x = 320
    
    def move(self):
        if pressed_keys[K_LEFT] and self.x >0:
            self.x-=3
        if pressed_keys[K_RIGHT] and self.x <540:
            self.x +=3

    def fire(self):
        missiles.append(Missile(self.x + 50))


    def draw(self):
        screen.blit(fighter_image,(self.x,591))

class Missile:
    def __init__(self, x):
        self.x = x
        self.y = 591

    def move(self):
        self.y -=5

    def off_bottom_screen(self):
        return self.y < -8

    def draw(self):
        screen.blit(missile_image,(self.x -4,self.y))
        # pygame.draw.line(screen,(255,0,0),(self.x,self.y),(self.x,self.y + 8),1)


# badguy = Badguy()
badguys=[]
fighter = Fighter()
missiles = []

 
# Detect key presses to carry out various actions (Exit the game, fire the missiles....)

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type ==QUIT: # or event.type == K_d 
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            fighter.fire()
    pressed_keys = pygame.key.get_pressed()

    if time.time()  - last_badguy_spawn_time > 0.5:
        badguys.append(Badguy())
        last_badguy_spawn_time = time.time()


    screen.fill((0,0,0))

    # Here's the main game loop :)
    i=0
    while i <len(badguys):
        badguys[i].move()
        badguys[i].bounce()
        badguys[i].draw()
        if badguys[i].off_bottom_screen(): # Once a badguy makes it off the bottom of the screen, remove from list
            del badguys[i]
            i-=1
        i+=1

    i = 0
    while i < len(missiles):
        missiles[i].move()
        missiles[i].draw()
        if missiles[i].off_bottom_screen(): # Once a badguy makes it off the bottom of the screen, remove from list
            del missiles[i]
            i -= 1
        i += 1

    i=0
    while i < len(badguys):
        j = 0
        while j <len(missiles):
            if badguys[i].touching(missiles[j]):
                badguys[i].score() # this calls the score function
                del badguys[i]
                del missiles[j]
                i -=1
                break
            j += 1
        i += 1


        # badguy = Badguy()

    fighter.move()
    fighter.draw()

    screen.blit(font.render("Score: "+str(score),True,(255,255,255)),(5,5))


    pygame.display.update()

    # This is just a comment added to see what Git Hub will do
    # Don't quite know what I was expecting? Probably that the system would 'sense' changes and inform me that a 'sync' would be needed.
    # Added to further test GitHub - 20180414
    # Another - 20180414