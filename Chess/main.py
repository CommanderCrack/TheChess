import pygame

pygame.init()

#creating a display
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Alternative Chess Game")

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)

#load buttons
start_img = pygame.image.load('Sprites/Start-button.png').convert_alpha()

#game_states
paused = False
#game Loop
Run = True
while Run:

    screen.fill((55, 72, 33))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False

    pygame.display.update()
