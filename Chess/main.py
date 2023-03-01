#libraries I will need:
import pygame
from pygame import mixer
pygame.init()
#import engine error:
import Engine
#creating a display:
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
        #Images[piece] = pygame.transform.scale(pygame.image.load("Chess_pieces/" + piece + ".png"), (square_size, square_size))
        Images[piece] = pygame.image.load("Chess/Sprites/Chess_Pieces/"+ piece+".png")
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

def main ():
    pygame.init()
    screen = pygame.display.set_mode((screen_height,screen_width ))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = Engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # stop regeneration of the valid moves every time.
    LoadImages()
    running = True
    drawGameState(screen, gs)
    square_select = () #no square selected initially. (row,col)
    player_clicks = [] # keep track of the clicks
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() # loc. of mouse x,y
                # find out where we clicked on
                col = location[0]//square_size
                row = location[1]//square_size
                if square_select == (row, col): # checks if the same square is being clicked.
                    square_select = ()
                    player_clicks = []
                else:
                    square_select = (row, col)
                    player_clicks.append(square_select) # append for both.
                if len(player_clicks) == 2:
                    move = Engine.Move(player_clicks[0],player_clicks[1], gs.board)
                    print(move.ChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i]) ### fix here
                            moveMade = True
                            square_select = () # resets user clicks
                            player_clicks = []
                        if not moveMade:
                            player_clicks = [square_select]
                        
            # listen to keys
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q: #undo when q pressed
                    gs.undolastmove()
                    moveMade = True

        if moveMade: 
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(fps)
        pygame.display.flip()
            

#load buttons
start_img = pygame.image.load('Chess/Sprites/Start-button.png').convert_alpha()
setting_img = pygame.image.load('Chess/Sprites/Settings Cog.png').convert_alpha()
guide_img = pygame.image.load('Chess/Sprites/Guide.png').convert_alpha()

#backgrounds
main_cb = pygame.image.load('Chess/Sprites/MenuChessBoard.png').convert()
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
                Run = False
                if __name__ == "__main__":
                    main()
                
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        #draws button
        screen.blit(self.image,(self.rect.x, self.rect.y))

# Creating buttons for the menu screen. 
start_button = Button(170, 200, start_img, 0.5)    
setting_button = Button(10, 10, setting_img, 0.1)
guide_button = Button(180, 325, guide_img, 0.1)

#game_states

paused = False

#draw the squares onto the board.

def drawGameState(screen, gs):
    drawBoard(screen) #draw squares onto the screen
    # potential piece highlighting, move suggestion.
    drawPieces(screen, gs.board) # draw pieces ontop of the squares.

def drawBoard(screen):
    colours = [pygame.Color("white"), pygame.Color("aquamarine")]
    #nested for loop
    for r in range(Dimension):
        for c in range(Dimension):
            #colour picker.
            colour = colours[((r+c)%2)]
            pygame.draw.rect(screen, colour, pygame.Rect(c*square_size, r*square_size, square_size, square_size))

#draws the pieces according to the game state from engine.
def drawPieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            #check for empty squares.
            if piece != "--":
                screen.blit(Images[piece], pygame.Rect(c*square_size, r*square_size, square_size, square_size))

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
            pygame.quit()
            exit()

    pygame.display.update()


#allows to import
