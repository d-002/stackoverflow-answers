import pygame
from pygame.locals import *

class Player:
    def __init__(self):
        self.x = 320
        self.y = 300
        self.x_speed = 0

        self.image = pygame.Surface((30, 50))
        self.image.fill((255, 0, 0))

    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_RIGHT]:
            self.x_speed += 3000 * time_passed
        if pressed[K_LEFT]:
            self.x_speed -= 3000 * time_passed
        self.x_speed *= 0.95**(100 * time_passed)
        
        self.x += self.x_speed * time_passed
        self.render()

    def render(self):
        w, h = self.image.get_size()
        screen.blit(self.image, (int(self.x - w / 2), int(self.y - h)))

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
time_passed = 0

player = Player()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.fill((240, 250, 255))
    pygame.draw.rect(screen, (0, 200, 100), Rect((0, 300), (640, 300)))
    player.move()
    
    pygame.display.flip()
    time_passed = clock.tick() / 1000
