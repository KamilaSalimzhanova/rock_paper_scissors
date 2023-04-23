import pygame, sys, math
from random import *
from pygame.locals import *

class Object():     #parent class
    def __init__(self, screen, path, currentX = None, currentY = None):
        self.screen = screen
        self.img = pygame.image.load(path)   
        self.rect = self.img.get_rect()             #getting a rectangle sized image
        self.screen_rect = self.screen.get_rect()   
        self.rect.topleft = (randint(0, 400-self.rect.width), randint(0, 600-self.rect.height)) if currentX == None else (currentX, currentY)
        self.direction = uniform(0, 2*math.pi)           #random floating-point number
        self.speed = 1                                   #random int of speed

    def output(self):
        self.screen.blit(self.img, self.rect)       #draw

    def move(self):
        #checking boundaries
        if self.rect.x <= 0 or self.rect.x + self.rect.width >= 380 or self.rect.left <= 0 or self.rect.right >= self.screen_rect.width:
            self.direction = 3.12 - self.direction
        if self.rect.y <= 0 or self.rect.y + self.rect.height >= self.screen_rect.height or self.rect.bottom >= self.screen_rect.height or self.rect.top <= 0:
            self.direction = -self.direction
       
        x_direction = self.speed * math.cos(self.direction)
        y_direction = self.speed * math.sin(self.direction)

        self.rect.x += x_direction
        self.rect.y += y_direction
    
    def change_direction(self, other):
        
        overlap_x = (self.rect.width + other.rect.width) / 2 - abs(self.rect.centerx - other.rect.centerx)
        overlap_y = (self.rect.height + other.rect.height) / 2 - abs(self.rect.centery - other.rect.centery)
            
        if overlap_x < overlap_y:
            if self.rect.centerx < other.rect.centerx:
                self.rect.right = other.rect.left - overlap_x
                other.rect.left = self.rect.right
            else:
                self.rect.left = other.rect.right + overlap_x
                other.rect.right = self.rect.left
            x_disp = other.rect.x - self.rect.x
            x_disp *= -1
            other.rect.x = self.rect.x + x_disp
        else:
            if self.rect.centery < other.rect.centery:
                self.rect.bottom = other.rect.top - overlap_y
                other.rect.top = self.rect.bottom
            else:
                self.rect.top = other.rect.bottom + overlap_y
                other.rect.bottom = self.rect.top
            y_disp = other.rect.y - self.rect.y
            y_disp *= -1
            other.rect.y = self.rect.y + y_disp

        self.move()
        
class Rock(Object):
    def __init__(self, screen, x = None, y = None):
        self.screen = screen
        super().__init__(self.screen, "pics/rock.png", x, y)
    
class Paper(Object):
    def __init__(self, screen, x = None, y = None):
        self.screen = screen
        super().__init__(self.screen, "pics/paper.png",  x, y)     

class Scissors(Object):
    def __init__(self, screen, x = None, y = None):
        self.screen = screen
        super().__init__(self.screen, "pics/scissors.png", x, y)   
           
pygame.init()    #initialization of the game
screen = pygame.display.set_mode((400, 600)) #size of the screen using tuple pygame.flags = NOFRAME
pygame.display.set_caption("Rock paper scissors")

icon = pygame.image.load("./pics/icon1.png")
pygame.display.set_icon(icon)

pygame.mixer.music.load("./pics/mozart-serenade-in-g-major_kA99wY7u.mp3")
pygame.mixer.music.play(-1) #infinite looping of music

bg = pygame.image.load("./pics/background.png")

clock = pygame.time.Clock()   #fps

rocks = [Rock(screen) for _ in range(randint(1, 10))]    #list comprehension
papers = [Paper(screen) for _ in range(randint(1, 10))]
scissors = [Scissors(screen) for _ in range(randint(1, 10))]

def win(img):
    myfont = pygame.font.SysFont('Raleway', 72, bold=True, italic=True)
    text = myfont.render("Win!", True, (0, 0, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.top = 10
    screen.fill((254, 242, 255))
    screen.blit(text, text_rect)
    screen.blit(pygame.image.load(img), (130, 180)) #128 pixels
    pygame.display.update()
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            sys.exit()
    screen.blit(bg, (0, 0)) #background
    
    if (len(rocks) == 0 and len(papers) == 0 and len(scissors) != 0):
        win('./pics/scissors_win.png')
    elif (len(rocks) == 0 and len(papers) != 0 and len(scissors) == 0):
        win('./pics/papers_win.png')
    elif (len(rocks) != 0 and len(papers) == 0 and len(scissors) == 0):
        win('./pics/rocks_win.png')
    
    print(len(rocks), ' ', len(papers), ' ', len(scissors))

    for rock in rocks:
        rock.move()
    for paper in papers:
        paper.move()
    for scissor in scissors:
        scissor.move() 
        
    remove_rocks = set()
    add_papers = set()

    for i in range(len(rocks)):
        for j in range(i+1, len(rocks)):
            if rocks[i].rect.colliderect(rocks[j].rect):
                rocks[i].change_direction(rocks[j])

    for i in range(len(papers)):    #paper X rock  => paper
        for j in range(len(rocks)):
            if papers[i].rect.colliderect(rocks[j].rect):
                rocks[j].change_direction(papers[i])
                current_x, current_y = rocks[j].rect.x, rocks[j].rect.y
                add_papers.add(Paper(screen, current_x, current_y))
                remove_rocks.add(rocks[j])

    for i in remove_rocks:
        rocks.remove(i)  
    papers.extend(list(add_papers)) 

    for i in range(len(papers)):
        for j in range(i+1, len(papers)):
            if papers[i].rect.colliderect(papers[j].rect):
                papers[i].change_direction(papers[j])

    add_scissors = set()
    remove_papers = set()
    for i in range(len(scissors)):    #scissors X paper  => scissor
        for j in range(len(papers)):
            if scissors[i].rect.colliderect(papers[j].rect):
                papers[j].change_direction(scissors[i])
                current_x, current_y = papers[j].rect.x, papers[j].rect.y
                add_scissors.add(Scissors(screen, current_x, current_y))
                remove_papers.add(papers[j])
    
    for i in remove_papers:
        papers.remove(i)  
    scissors.extend(list(add_scissors)) 
    
    for i in range(len(scissors)):
        for j in range(i+1, len(scissors)):
            if scissors[i].rect.colliderect(scissors[j].rect):
                scissors[i].change_direction(scissors[j])

    add_rocks = set()
    remove_scissors = set()
    for i in range(len(rocks)):    #rock X scissors  => rock
        for j in range(len(scissors)):
            if rocks[i].rect.colliderect(scissors[j].rect):
                scissors[j].change_direction(rocks[i])
                current_x, current_y = scissors[j].rect.x, scissors[j].rect.y
                add_rocks.add(Rock(screen, current_x, current_y))
                remove_scissors.add(scissors[j])

    for i in remove_scissors:
        scissors.remove(i)  
    rocks.extend(list(add_rocks)) 

    for rock in rocks:
        rock.output() 
    for paper in papers:
        paper.output()
    for scissor in scissors:
        scissor.output()

    pygame.display.update()
    clock.tick(60) 