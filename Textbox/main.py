def inputbox(pos, text, active):
    input_box = Rect(pos, (200, 40))
    
    if pygame.mouse.get_pressed()[0]: # active the textbox by clicking on it
        if input_box.collidepoint(pygame.mouse.get_pos()):
            active = True
        else:
            active = False
        
    for event in events:
        if event.type == KEYDOWN and active:
            if event.key == K_BACKSPACE:
                text = text[:-1] # delete last character
            else:
                try:
                    ord(event.unicode) # raise error if not a printable character (e.g. Ctrl)
                                       # so that no strange symbol is written instead
                    text += event.unicode
                except:
                    pass
        
    screen.blit(textbox_image, pos)

    if active and int(time.time() * 2) % 2:
        blink = '_'
    else:
        blink = ''
        
    text_surf = font.render(text + blink, 0, (255, 255, 255))
    screen.blit(text_surf, (pos[0] + 12, pos[1] + 12))
    
    text_width = font.render(text, 0, (0, 0, 0)).get_width()
    while text_width > 176:
        text = text[:-1] # if the text is too long, remove last character
        text_width = font.render(text, 0, (0, 0, 0)).get_width()
    return text, active

import pygame
import time
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((240, 80))
font = pygame.font.SysFont('consolas', 20, True)

textbox_image = pygame.Surface((200, 40))
text = ''
active = False

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))

    text, active = inputbox((20, 20), text, active)

    pygame.display.flip()
