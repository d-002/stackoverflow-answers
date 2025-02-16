import pygame
from pygame.locals import *
from math import sin

pygame.init()
clock = pygame.time.Clock()
time_passed = 0
screen = pygame.display.set_mode((640, 480))

class Map:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self):
        self.x = min(max(self.x, player.x - 2 * 640 / 3), player.x - 640 / 3)
        self.y = min(max(self.y, player.y - 2 * 480 / 3), player.y - 480 / 3)

        screen.fill((153, 217, 234))
        for x in range(640):
            size = int(sin((self.x + x) / 200) * 100) + 300
            pygame.draw.line(screen, (34, 177, 76), (x, size - int(self.y)), (x, 640))

class Player:
    def __init__(self):
        self.x = 320
        self.y = 240
        self.image = pygame.Surface((50, 50), SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (25, 25), 25)

    def update(self):
        self.y = sin((self.x) / 200) * 100 + 300
        
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.x -= 500 * time_passed
        if keys[K_RIGHT]:
            self.x += 500 * time_passed

        screen.blit(self.image, (int(self.x - map.x - 25), int(self.y - map.y - 50)))

map = Map()
player = Player()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    map.update()
    player.update()

    pygame.display.flip()
    time_passed = clock.tick() / 1000
