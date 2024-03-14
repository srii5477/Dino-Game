import pygame
import sys

# to generate enemies
import random

''' tasks:
1. load up starting screen
2. position and display the starting text
3. maintain a score
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

                
# setting up game screen
WIDTH = 600
HEIGHT = 800

# curr = GameState.INTRO
# set up a clock to slow down the frame rate
clock = pygame.time.Clock()
main_sound = pygame.mixer.Sound("retro-wave-style-track-59892.mp3")
main_sound.play()

collision_sound = pygame.mixer.Sound("arcade-bleep-sound-6071.mp3")
# extend pygame.sprite.Sprite using super() (inheritance, returns a delegate object to the parent and extends its functionality)
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.limit = 5
        self.passbys = 0
        main_sound.play()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.avatar = pygame.Surface((PLAYER_X, PLAYER_Y))
        #self.avatar.fill((0, 0, 0))
        self.avatar = pygame.image.load("right.png").convert_alpha()
        self.avatar.set_colorkey((255, 255, 255))
        self.avatar = pygame.transform.smoothscale(self.avatar, (100, 150))
        self.rect = self.avatar.get_rect(
            center = (
                20,
                HEIGHT/2
            )
        )
        self.score = 0
    def update(self, pressed):
        if pressed[pygame.K_UP]:
            self.rect.move_ip(0, -10)
        if pressed[pygame.K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed[pygame.K_RIGHT]:
            self.rect.move_ip(10, 0)
        if pressed[pygame.K_LEFT]:
            self.rect.move_ip(-10, 0)
        # prevent player from hurtling off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH - 25
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT - 25
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 20
        self.y = 10
        #self.avatar = pygame.Surface((self.x, self.y))
        #self.avatar.fill((45, 60, 0))
        self.avatar = pygame.image.load("enemy.jpg").convert()
        self.avatar.set_colorkey((255, 255, 255))
        self.avatar = pygame.transform.scale(self.avatar, (80, 80))
        self.rect = self.avatar.get_rect(
            center = (
                random.randint(WIDTH + 20, WIDTH + 100),
                random.randint(0, HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        
screen = pygame.display.set_mode([HEIGHT, WIDTH]) # provide a list or tuple to define the screen size
pygame.display.set_caption("Dodge the Ball!")
game = Game()
''' now we have to create a steady supply of enemies aka obstacles at regular intervals- create a custom event
and set its interval '''
ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 1000)

# handle game running
while True: # game loop- controls whether the program should be running or when it should quit
    # if user clicks exit window quit game
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            # game_state = 0
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # game_state = 0
                pygame.quit()
                sys.exit()
            ''' else:
                player.update(event) '''
        elif event.type == ADD_ENEMY:
                new_enemy = Enemy()
                game.enemies.add(new_enemy)
                game.all_sprites.add(new_enemy)
                game.passbys += 1
                if game.passbys > game.limit:
                    game.player.score += 5
                    game.limit += 5
                print(game.player.score)
                
    pressed = pygame.key.get_pressed()
    game.player.update(pressed) 
    game.enemies.update()  
        # fill background color of screen: either a list or tuple is its argument
    #screen.fill((137, 13, 15))
    background = pygame.image.load("bgimage.jpg")
    background = pygame.transform.scale(background, (HEIGHT, WIDTH))
    screen.fill((255, 255, 255))
    bg_rect = background.get_rect()
    screen.blit(background, bg_rect)
        # simply draw a circle on the screen
        # pygame.draw.circle(screen, (0, 0, 0), (250, 250), 75)
    ''' surf = pygame.Surface([100, 100])
        surf.fill((0, 0, 0))
        rect = surf.get_rect()
        screen.blit(surf, ((HEIGHT - surf.get_height())/2, (WIDTH - surf.get_width())/2)) ''' # to center our object
    
    #screen.blit(player.avatar, player.rect)
    for entity in game.all_sprites:
        screen.blit(entity.avatar, entity.rect)
    # check for collisions
    if pygame.sprite.spritecollideany(game.player, game.enemies):
        # you lose! try again page
        game.player.kill()
        main_sound.stop()
        collision_sound.play()
        loser = pygame.font.Font('Micro5-Regular.ttf', 50)
        new_surf = loser.render(f"You lost! Your final score is {game.player.score}.", False, (255, 68, 51)) # create a surface off the text
        screen.blit(new_surf, (WIDTH/3, HEIGHT/2))
        pygame.display.flip()
        pygame.time.wait(1000)
        screen = pygame.display.set_mode([HEIGHT, WIDTH])
        screen.fill((144, 238, 144))
        intro_screen = pygame.font.Font('Micro5-Regular.ttf', 70)
        intro = intro_screen.render("Try again? Press ESC to exit or wait to restart", False, (255, 68, 51))
        screen.blit(intro, (10, HEIGHT/5))
        pygame.display.flip()
        pygame.time.wait(2000)
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        else:
            game = Game()
            continue
        # flip display- updates contents of display to the screen, without this nothing appears
    pygame.display.flip()
    clock.tick(30) # program should maintain a rate of 30 fps

    
