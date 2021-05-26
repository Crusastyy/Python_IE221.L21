from pygame.constants import NOEVENT
from cotuong_const import BLOCKING_RULES, board_matrix, start_coords_2, INVALID_POS, board_coor, location_chess
from copy import deepcopy
from verify import Advisor, Cannon, Elephant, King, Horse, Pawn, Rock

BOARD_MATRIX = deepcopy(board_matrix)
STARTCOORDS = deepcopy(start_coords_2)

notation_to_object = {
    'a': Advisor, 
    'c': Cannon, 
    'e': Elephant, 
    'k': King,
    'h': Horse,
    'p': Pawn,
    'r': Rock
}

def is_fen(load):
    return load is None


def is_dict(load):
    dict_format = []  # format like start_coords_2
    return isinstance(load, dict) and dict_format is not None


class GameState(object):
    def __init__(self, load=''):
        self.SYMBOLS = 'acekhprACEKHPR'
        self.next_move = 'b'
        self.turn = 1
        self.board_matrix = deepcopy(BOARD_MATRIX)
        self.__start_coords = deepcopy(STARTCOORDS)
        self.piece_list = []
        self.__load_game(load)
        self.history = []

    def get_left_first_piece(self, position):
        for i in range(position - 1, position - (position%10), - 1):
            current = None
            for piece in self.piece_list:
                if piece.position == i:
                    current = piece
            if current != None:
                return current


    def get_right_first_piece(self, position):
        for i in range(position + 1, position + 10 - (position%10), + 1):
            current = None
            for piece in self.piece_list:
                if piece.position == i:
                    current = piece
            if current != None:
                return current


    def get_top_first_piece(self, position):
        for i in range(position - 10, 10, - 10):
            current = None
            for piece in self.piece_list:
                if piece.position == i:
                    current = piece
            if current != None:
                return current


    def get_bottom_first_piece(self, position):
        for i in range(position + 10, 110, + 10):
            current = None
            for piece in self.piece_list:
                if piece.position == i:
                    current = piece
            if current != None:
                return current

    def get_left_second_piece(self, position):
        count = 0
        for i in range(position - 1, position - (position%10), - 1):
            current = None
            for piece in self.piece_list:
                if piece.position == i:
                    current = piece
            if current != None:
                if count == 1:
                    return current
                else: 
                    count += 1


    def get_right_second_piece(self, position):
        count = 0
        for i in range(position - 1, position + 10 - (position%10), + 1):
            current = None
            for piece in self.piece_list:
                if piece.position == i:
                    current = piece
            if current != None:
                if count == 1:
                    return current
                else: 
                    count += 1

    def get_top_second_piece(self, position):
        count = 0
        for i in range(position - 10, 10 , - 10):
            current = None
            for piece in self.piece_list:
                if piece.position == i:
                    current = piece
            if current != None:
                if count == 1:
                    return current
                else: 
                    count += 1
    
    def get_bottom_second_piece(self, position):
        count = 0
        for i in range(position + 10, 110, + 10):
            current = None
            for piece in self.piece_list:
                if piece.position == i:
                    current = piece
            if current != None:
                if count == 1:
                    return current
                else: 
                    count += 1

    def calc_moving_list(self, piece):
        position = piece.position
        left = self.get_left_first_chessman(position)
        right = self.get_right_first_chessman(position)
        top = self.get_top_first_chessman(position)
        bottom = self.get_bottom_first_chessman(position)

        piece.calc_moving_path(left, (left.position if left != None else None),piece.position, 1, 0, True)
        piece.calc_moving_path(right, (right.position if right != None else None),piece.position, -1, 8, True)
        piece.calc_moving_path(top, (top.position if top != None else None),piece.postion, -1, 9, False)
        self.calc_moving_path(bottom, (bottom.position if bottom != None else None),piece.position, 1, 0, False)


    def __generate_piece_list_from_position_list(self, piece_name):
        return [notation_to_object[piece_name.lower()](name=piece_name, pos_id=id) for id in range(len(self.__start_coords[piece_name]))]

    def __generate_piece_list(self):
        return [piece for piece_name in self.SYMBOLS for piece in self.__generate_piece_list_from_position_list(piece_name)]

    def __generate_simple_current_turn_state(self):
        return [piece.current_state for piece in self.piece_list]

    def __new_game(self):
        self.next_move = 'b'
        self.turn = 1
        self.piece_list = self.__generate_piece_list()
        self.location = deepcopy(location_chess)
        for piece in self.piece_list:
            self.location[(piece.position // 10) - 1][(piece.position % 10) - 1] = 1
        return 'New game has been set.'

    def calc_pos_list(self, piece):
        pos = []
        name = piece.name.lower()
        if name == 'a':
            pass
        elif name == 'c':
            pass
        elif name == 'e':
            pass
        return pos

    def is_occupied(self,piece, next_pos): 
        blocked_destination = False 
        blocked_enroute     = False 
        opposite_side_destination = False
        pos_list = set([pos for rule in piece.blocking_rules for pos in rule(curr_pos=piece.position, target_pos=next_pos)])

        another_piece = self.get_piece_with_position(next_pos)
        if another_piece is not None: 
            blocked_destination = True 
            opposite_side_destination = not ((piece.name.isupper() and another_piece.name.isupper()) and (piece.name.islower() and another_piece.name.islower()))
        pos_list.remove(next_pos)
        
        if piece.name.lower() != 'c':
            for pos in pos_list: 
                another_piece = self.get_piece_with_position(pos)
                if  another_piece is not None:
                    blocked_enroute = True 
                    break 
        else:
            count_c = 0
            for pos in pos_list: 
                enroute_piece = self.get_piece_with_position(pos)
                if enroute_piece is not None:
                    count_c += 1
                    if(count_c == 1):
                        blocked_enroute = False 
                        if another_piece is None:
                            blocked_enroute = True 
                            break
                    elif count_c > 1:
                        blocked_enroute = True
                        break
            if count_c == 0:
                opposite_side_destination = False 
            

        return blocked_destination, blocked_enroute, opposite_side_destination

    def get_piece_with_position(self, value):
        return next((x for x in self.piece_list if x.position == value), None)

    def get_piece_with_id(self, value):
        return next((x for x in self.piece_list if x.id == value), None)

    def new_game(self):
        return self.__new_game()

    def current_turn(self):
        return self.board_matrix

    @property
    def start_coords(self):
        return self.__start_coords

    def __load_game(self, load):
        if load == '':
            self.__new_game()
        elif is_fen(load):
            pass
        elif is_dict(load):
            pass
        else:
            raise ValueError('Unrecognized string to load')

    def __recieve_new_move(self):
        return None

    def __update_piece_list(self):
        return 

    def __update_history(self):
        self.history.append(self.__generate_simple_current_turn_state())

    def update_move(self, piece_id, next_pos):
        is_updated = False 
        try: 
            piece = self.get_piece_with_id(piece_id)        

            if piece.valid_move(next_pos):
                is_destination_blocked, is_enroute_blocked, is_edible = self.is_occupied(piece=piece, next_pos=next_pos)
                if not is_enroute_blocked:
                    if is_destination_blocked and is_edible:
                        self.piece_list.remove(self.get_piece_with_position(next_pos))
                        piece.position = next_pos 
                        piece.coor = board_coor[piece.position]
                        is_updated = True
                    elif not is_destination_blocked:
                        piece.position = next_pos 
                        piece.coor = board_coor[piece.position]
                        is_updated = True         
            elif piece.name.lower() == 'k':
                another_piece = self.get_piece_with_position(next_pos)
                if another_piece != None:
                    if piece.name != another_piece and piece.name.lower() == another_piece.name.lower():
                        is_destination_blocked = False 
                        is_enroute_blocked     = False 
                        is_edible = False
                        
                        if (abs(next_pos - piece.position) % 10 == 0):

                            pos_list =  list(range(piece.position + 10, next_pos - 1, 10)) if next_pos > piece.position else list(range(next_pos + 10, piece.position - 1, 10)),

                        
                        if another_piece is not None: 
                            is_destination_blocked = True 
                            is_edible = not ((piece.name.isupper() and another_piece.name.isupper()) and (piece.name.islower() and another_piece.name.islower()))
                        
                        
                       
                        for pos in pos_list: 
                            another_piece = self.get_piece_with_position(pos)
                            if  another_piece is not None:
                                is_enroute_blocked = True 
                                break 
                          

                        
                        if not is_enroute_blocked:
                            if is_destination_blocked and is_edible:
                                self.piece_list.remove(self.get_piece_with_position(next_pos))
                                piece.position = next_pos 
                                piece.coor = board_coor[piece.position]
                                is_updated = True
                            elif not is_destination_blocked:
                                piece.position = next_pos 
                                piece.coor = board_coor[piece.position]
                                is_updated = True                      
        except AttributeError: 
            print('No piece with this id')

        return is_updated

    def turn_mananger(self):
        self.__update_history() 
        self.turn += 1 


if __name__ == "__main__": 
  
    from pprint import PrettyPrinter as pp 
    newgame = GameState() 
    pp().pprint(Pawn('P', 2).valid_move(65))
    pp().pprint(newgame.is_occupied(newgame.get_piece_with_id('P2'), 65))
    pp().pprint(newgame.update_move('P2', 65))
    pp().pprint(newgame.piece_list)
    for piece in newgame.piece_list:
        pp().pprint(str(piece.row)+"-"+str(piece.col))