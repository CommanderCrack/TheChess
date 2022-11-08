import pygame

pygame.init()

#creating a display
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Alternative Chess Game")

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)

#load buttons

start_img = pygame.image.load('Sprites/Start-button.png').convert_alpha()
setting_img = pygame.image.load('Sprites/Settings Cog.png').convert_alpha()
guide_img = pygame.image.load('Sprites/Guide.png').convert_alpha()

#backgrounds
main_cb = pygame.image.load('Sprites/Chess_Board.png').convert()
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
        
    
    def draw(self):
        #draws button
        screen.blit(self.image,(self.rect.x, self.rect.y))
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouse over and clicked on button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                print("clicked")
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

            
        

start_button = Button(205, 200, start_img, 0.5)    
setting_button = Button(10,10, setting_img, 0.1)
guide_button = Button(215,325, guide_img, 0.1)

#game_states
paused = False
#game Loop
while True:
    screen.fill((55, 72, 33))
    screen.blit(main_cb,(0,0))
    start_button.draw()
    setting_button.draw()
    guide_button.draw()
    
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
