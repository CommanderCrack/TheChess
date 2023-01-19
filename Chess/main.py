#libraries I will need:
import pygame
pygame.init()
#import engine error.
import Engine
#creating a display
screen_width = 512
screen_height = 512
Dimension = 8
square_size = screen_height // Dimension
fps = 15 
Images = {}
#loading images with the exception of the cannon and spider.
def LoadImages():
    pieces = ['wp','wN','wB','wK','wQ','wR','bp','bN','bB','bK','bQ','bR']
    for piece in pieces:
        Images[pieces] = pygame.transform.scale(pygame.image.load("TheChess/Chess/Sprites/Chess_pieces/" + piece + ".png"), (square_size, square_size))

# font and text
MenuFont = pygame.font.Font('freesansbold.ttf',32)
MenuTextX = 200
MenuTextY = 100
textCol = (0,0,0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Alternative Chess Game")

#draw text onto screen 
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#load buttons
start_img = pygame.image.load('TheChess/Chess/Sprites/Start-button.png').convert_alpha()
setting_img = pygame.image.load('TheChess/Chess/Sprites/Settings Cog.png').convert_alpha()
guide_img = pygame.image.load('TheChess/Chess/Sprites/Guide.png').convert_alpha()

#backgrounds
main_cb = pygame.image.load('TheChess/Chess/Sprites/MenuChessBoard.png').convert()
main_cb = pygame.transform.scale(main_cb, (600,600))

#button class
class Button():
    def __init__(self, x , y , image , scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    # special draw function for buttons, includes self.clicked check.
    def draw(self):
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouse over and clicked on button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                print("clicked")
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draws button
        
        screen.blit(self.image,(self.rect.x, self.rect.y))

# Creating buttons for the menu screen. 
start_button = Button(218, 200, start_img, 0.5)    
setting_button = Button(10,10, setting_img, 0.1)
guide_button = Button(224,325, guide_img, 0.1)

#game_states
paused = False

def main ():
    pygame.init()
    screen = pygame.display.set_mode((screen_height,screen_width ))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = Engine.GameState()
    LoadImages()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        clock.tick(fps)
        pygame.display.flip()

Run = True
while Run:
    screen.fill((55, 72, 33))
    screen.blit(main_cb,(0,0))
    start_button.draw()
    setting_button.draw()
    guide_button.draw()
    draw_text("Chess Game", MenuFont, textCol, MenuTextX, MenuTextY)
    #event handler within main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False

    pygame.display.update()
