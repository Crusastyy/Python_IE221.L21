import pygame, sys
from pygame.locals import * 
import bGround
import cotuong
from cotuong_const import board_matrix, start_coords_2, INVALID_POS
from copy import deepcopy
from verify import Advisor, Cannon, Elephant, King, Horse, Pawn, Rock

def translate_hit_area(screen_x, screen_y):
    return screen_x // 80, screen_y // 80

def select_chessman_from_list(piece_list, col, row):
    for piece in piece_list:
        if piece.row == row and piece.col == col:
            return piece

class Graphiccc():
    def __init__(self):
        self.res = (800, 800)
        pygame.init()
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Co tuong")
        self.bg = bGround.Background()

    def Drawbg(self):
        self.screen.fill((255,255,255))
        self.bg.draw(self.screen)

    def DrawPiece(self, pieceList):
        for piece in pieceList:
            self.screen.blit(piece.img, (piece.coor[0]-40, piece.coor[1]-40))

from pprint import PrettyPrinter as pp 
if __name__ == '__main__':
    FPS = 20
    fpsClock = pygame.time.Clock()
    gp = Graphiccc()
    newgame = cotuong.GameState()
    current_chessman = None


    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
            elif ev.type == MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if index == 0 and pressed_array[index]:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        col_num, row_num = translate_hit_area(mouse_x, mouse_y)
                        chessman_sprite = select_chessman_from_list(newgame.piece_list, col_num, row_num)
                        if current_chessman is None and chessman_sprite != None:
                            if chessman_sprite.name.islower() != newgame.turn%2==1:
                                current_chessman = chessman_sprite
                                chessman_sprite.is_selected = True
                        elif current_chessman != None and chessman_sprite != None:
                            if chessman_sprite.name.islower() != newgame.turn%2==1:
                                current_chessman.is_selected = False
                                current_chessman = chessman_sprite
                                chessman_sprite.is_selected = True
                            else:
                                success = current_chessman.valid_move(board_matrix[row_num+1][col_num+1])
                                if success:
                                    newgame.update_move(current_chessman.id, board_matrix[row_num+1][col_num+1])
                                    current_chessman.is_selected = False
                                    current_chessman = None
                        elif current_chessman != None and chessman_sprite is None:
                            success = current_chessman.valid_move(board_matrix[row_num+1][col_num+1])
                            if success:
                                newgame.update_move(current_chessman.id, board_matrix[row_num+1][col_num+1])
                                current_chessman.is_selected = False
                                current_chessman = None

        gp.Drawbg()
        mouse = pygame.mouse.get_pos()
        gp.DrawPiece(newgame.piece_list)
        pygame.display.update()
        fpsClock.tick(FPS)