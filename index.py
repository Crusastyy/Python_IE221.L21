import pygame, sys
from pygame.locals import * 
import bGround
import cotuong
from cotuong_const import board_matrix, start_coords_2, INVALID_POS, WHITE, GREEN, RED
from copy import deepcopy
from verify import Advisor, Cannon, Elephant, King, Horse, Pawn, Piece, Rock
import os 
import pygame_menu


def translate_hit_area(screen_x, screen_y):
    return screen_x // 80, screen_y // 80

def select_chessman_from_list(piece_list, col, row):
    for piece in piece_list:
        if piece.position == board_matrix[row + 1][col + 1]:
            return piece

def set_difficulty(value, difficulty):
    # Do the job here !
    if difficulty == 2:
        newgame.AI = True
    else: 
        newgame.AI = False

def start_the_game():
    # Do the job here !
    AI = False
    FPS = 20
    fpsClock = pygame.time.Clock()
    current_state = True
    current_chessman = None
    victor_message = ''
   

    if not newgame.AI:
        while current_state:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == MOUSEBUTTONDOWN:
                    pressed_array = pygame.mouse.get_pressed()
                    for index in range(len(pressed_array)):
                        if index == 0 and pressed_array[index]:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            col_num, row_num = translate_hit_area(mouse_x, mouse_y)
                            chessman_sprite = select_chessman_from_list(newgame.piece_list, col_num, row_num)
                            if current_chessman is None and chessman_sprite != None:
                                if chessman_sprite.name.islower() != (newgame.turn%2==1):
                                    current_chessman = chessman_sprite
                                    chessman_sprite.is_selected = True
                            elif current_chessman != None and chessman_sprite != None:
                                if chessman_sprite.name.islower() != (newgame.turn%2==1):
                                    current_chessman.is_selected = False
                                    current_chessman = chessman_sprite
                                    chessman_sprite.is_selected = True
                                else:
                                    #success = current_chessman.valid_move(board_matrix[row_num+1][col_num+1])
                                    success = newgame.update_move(current_chessman.id, board_matrix[row_num+1][col_num+1])
                                    if success:
                                        newgame.turn_mananger()
                                        current_chessman.is_selected = False
                                        current_chessman = None
                                        if chessman_sprite.name.lower() == 'k':
                                            if chessman_sprite.name.islower() and (newgame.turn % 2 == 0):
                                                victor_message = "Red win"
                                            else:
                                                victor_message = "Black win"
                                                
                            elif current_chessman != None and chessman_sprite is None:
                                #success = current_chessman.valid_move(board_matrix[row_num+1][col_num+1])
                                success =  newgame.update_move(current_chessman.id, board_matrix[row_num+1][col_num+1])
                                if success:
                                    newgame.turn_mananger()
                                    current_chessman.is_selected = False
                                    current_chessman = None

            if (victor_message == ''):
                gp.Drawbg()
                gp.DrawPiece(newgame.piece_list)
            else: 
                gp.DrawVictorScreen(victor_message)
            mouse = pygame.mouse.get_pos()    
            pygame.display.update()
            fpsClock.tick(FPS)
    
    else:
        while current_state:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == MOUSEBUTTONDOWN:
                    pressed_array = pygame.mouse.get_pressed()
                    for index in range(len(pressed_array)):
                        if index == 0 and pressed_array[index]:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            col_num, row_num = translate_hit_area(mouse_x, mouse_y)
                            chessman_sprite = select_chessman_from_list(newgame.piece_list, col_num, row_num)
                            if current_chessman is None and chessman_sprite != None:
                                if chessman_sprite.name.islower() != (newgame.turn%2==1):
                                    current_chessman = chessman_sprite
                                    chessman_sprite.is_selected = True
                            elif current_chessman != None and chessman_sprite != None:
                                if chessman_sprite.name.islower() != (newgame.turn%2==1):
                                    current_chessman.is_selected = False
                                    current_chessman = chessman_sprite
                                    chessman_sprite.is_selected = True
                                else:
                                    #success = current_chessman.valid_move(board_matrix[row_num+1][col_num+1])
                                    success = newgame.update_move(current_chessman.id, board_matrix[row_num+1][col_num+1])
                                    if success:
                                        newgame.turn_mananger()
                                        current_chessman.is_selected = False
                                        current_chessman = None
                                        if chessman_sprite.name.lower() == 'k':
                                            if chessman_sprite.name.islower() and (newgame.turn % 2 == 0):
                                                victor_message = "Red win"
                                            else:
                                                victor_message = "Black win"
                                                
                            elif current_chessman != None and chessman_sprite is None:
                                #success = current_chessman.valid_move(board_matrix[row_num+1][col_num+1])
                                success =  newgame.update_move(current_chessman.id, board_matrix[row_num+1][col_num+1])
                                if success:
                                    newgame.turn_mananger()
                                    current_chessman.is_selected = False
                                    current_chessman = None

            

            if (victor_message == ''):
                gp.Drawbg()
                gp.DrawPiece(newgame.piece_list)
            else: 
                gp.DrawVictorScreen(victor_message)
            mouse = pygame.mouse.get_pos()    
            pygame.display.update()
            if newgame.turn % 2 == 0:
                victor_message = newgame.generateAIMove()
            fpsClock.tick(FPS)


class Graphiccc():
    def __init__(self):
        self.res = (800, 800)
        pygame.init()
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Co tuong")
        self.bg = bGround.Background()
        
    def DrawStartMenu(self):
        self.menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input('Name :', default='Phuc Thinh')
        self.menu.add.selector('Difficulty :', [('2 Player', 1), ('Easy AI', 2)], onchange=set_difficulty)
        self.menu.add.button('Play', start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(gp.screen)

    def Drawbg(self):
        self.font = pygame.font.Font('freesansbold.ttf', 14)
        self.screen.fill((255,255,255))
        self.bg.draw(self.screen)
        self.textSurface = self.font.render("Undo", True, GREEN, RED)
        self.screen.blit(self.textSurface ,(750, 50))
        
    def DrawPiece(self, pieceList):
        for piece in pieceList:
            if piece.is_selected:
                if piece.is_transparent:
                    piece.img = piece.trans_img
                else:
                    piece.img = piece.tam
                piece.is_transparent = not piece.is_transparent
            else:
                piece.img = piece.tam
            self.screen.blit(piece.img, (piece.coor[0]-40, piece.coor[1]-40))

    def tam(self, piece_list):
        for piece in piece_list:
            piece.tam = piece.img

    def DrawVictorScreen(self, message):
        self.screen.fill(WHITE)

  
        self.menu = pygame_menu.Menu(300, 400, 'Result',
                        theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.label(message, max_char = -1, font_size =32)
        self.menu.add.button('Reset', main)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(self.screen)

def main():
    
    
    newgame.new_game()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 0)
    
    gp.tam(newgame.piece_list)

    gp.DrawStartMenu()

from pprint import PrettyPrinter as pp 
if __name__ == '__main__':
    newgame = cotuong.GameState()
    gp = Graphiccc()
    main()
    
    

    

    