import pygame
import sys

# to generate enemies
import random

''' tasks:
1. load up starting screen
2. position and display the starting text
'''

''' google duck game:
1. move from left to right on the screen
2. random obstacles coming from right to left
3. use arrow keys left, right, up, down to avoid obstacles
4. no score, no time constraints
5. game ends when either user closes the window, or hits obstacle
'''

# initializing pygame library- allows pygame to connects its abstractions to my hardware
pygame.init()
PLAYER_X = 75
PLAYER_Y = 25
# extend pygame.sprite.Sprite using super() (inheritance, returns a delegate object to the parent and extends its functionality)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.avatar = pygame.Surface((PLAYER_X, PLAYER_Y))
        self.avatar.fill((0, 0, 0))
        self.rect = self.avatar.get_rect()
        self.x = PLAYER_X
        self.y = PLAYER_Y
    def update(self, pressed):
        if pressed[pygame.K_UP]:
            self.y -= 5
        if pressed[pygame.K_DOWN]:
            self.y += 5
        if pressed[pygame.K_RIGHT]:
            self.x += 5
        if pressed[pygame.K_LEFT]:
            self.x -= 5
        # prevent player from hurtling off screen
        if self.x < 0:
            self.x = 0
        if self.y <= 0:
            self.y = 0
        if self.x > WIDTH:
            self.x = WIDTH - 25
        if self.y >= HEIGHT:
            self.y = HEIGHT - 25
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init()
        self.x = 20
        self.y = 10
        self.avatar = pygame.Surface((self.x, self.y))
        self.avatar.fill((45, 60, 0))
        self.rect = self.avatar.get_rect(
            center = (
                random.randint(WIDTH + 20, WIDTH + 100),
                random.randint(0, HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)
    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.kill()
        
                
# setting up game screen
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode([HEIGHT, WIDTH]) # provide a list or tuple to define the screen size
pygame.display.set_caption("Google Internetless Game")
player = Player()
# handle game running
while True: # game loop- controls whether the program should be running or when it should quit
    # if user clicks exit window quit game
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            ''' else:
                player.update(event) '''
                
    pressed = pygame.key.get_pressed()
    player.update(pressed)   
        # fill background color of screen: either a list or tuple is its argument
    screen.fill((137, 13, 15))
        # simply draw a circle on the screen
        # pygame.draw.circle(screen, (0, 0, 0), (250, 250), 75)
    ''' surf = pygame.Surface([100, 100])
        surf.fill((0, 0, 0))
        rect = surf.get_rect()
        screen.blit(surf, ((HEIGHT - surf.get_height())/2, (WIDTH - surf.get_width())/2)) ''' # to center our object
    
    screen.blit(player.avatar, (player.x, player.y))
        # flip display- updates contents of display to the screen, without this nothing appears
    pygame.display.flip()

    
