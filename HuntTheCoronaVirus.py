# Import and Initialization
import random
import time

import pygame
from pygame.locals import *

pygame.init()

number_virus = 5

# Display
size = (768, 432)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Jag das Corana Virus')
corona_size = [14400, 8100]


# Entities
class Virus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/virus.png')
        # random size of picture
        self.scale = random.randint(100, 200)
        self.image = pygame.transform.scale(self.image, (corona_size[0] // self.scale, corona_size[1] // self.scale))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound('sound/spray.mp3')
        # random position
        self.rect.left = random.randint(100, 668)
        self.rect.top = random.randint(100, 332)
        # random speed but not null
        self.speed = [random.randint(-5, 5), random.randint(-5, 5)]
        if self.speed[0] == 0:
            self.speed[0] += 1
        if self.speed[1] == 0:
            self.speed[1] += 1

    def flee(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < -20 or self.rect.right > size[0] + 20:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > size[1]:
            self.speed[1] = -self.speed[1]

    def cry(self):
        self.sound.play()

    def hit(self, pos):
        return self.rect.collidepoint(pos)

    def remove(self):
        self.image = pygame.transform.scale(self.image, (0, 0))
        self.rect = self.image.get_rect()


class Sprayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/spray.png')
        self.image = pygame.transform.scale(self.image, (21, 86))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


# Action --> Alter
# Assign Variables
sprite_group = pygame.sprite.Group()

viruses = []
for i in range(number_virus):
    viruses.append(Virus())

for virus in viruses:
    sprite_group.add(virus)

sprayer = Sprayer()
sprite_group.add(sprayer)

bg = pygame.Surface(size)
bg = bg.convert()
bg.fill((0, 0, 0))

bg_drosten = pygame.image.load('images/drosten.jpg')
bg = pygame.transform.scale(bg, size)

font = pygame.font.Font(None, 25)

keepGoing = True
gameOver = False
ctr = 0
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT, 200)
start_time = time.time()
elapsed_time = 0
display_time = 0
end_sound = pygame.mixer.Sound('sound/laugh.wav')

# Loop
while keepGoing:

    # Timer
    if not gameOver:
        clock.tick(30)
        elapsed_time = time.time() - start_time
    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            keepGoing = False
            break
        elif event.type == MOUSEBUTTONDOWN:
            for virus in viruses:
                if virus.hit(pygame.mouse.get_pos()):
                    virus.cry()
                    ctr += 1
                    virus.remove()
                    if ctr == number_virus:
                        end_sound.play()
                        gameOver = True
                    break
        elif event.type == USEREVENT:
            for virus in viruses:
                virus.flee()

            pygame.time.set_timer(USEREVENT, 15)

            screen.blit(bg, (0, 0))

            sprite_group.update()

            sprite_group.draw(screen)

            display_time = int(elapsed_time)

            text = font.render(u'verstrichene Zeit: ' + str(display_time) + ' Sekunden', True, Color('white'))
            screen.blit(text, (0, 0))

    if gameOver:
        screen.blit(bg_drosten, (0, 0))
        text = font.render(u'Danke fürs Aufräumen in ' + str(display_time) + ' Sekunden', True, Color('red'))
        screen.blit(text, (425, 300))
        clock.tick(0)

    # Redisplay
    pygame.display.flip()
