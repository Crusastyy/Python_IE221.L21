from cotuong_const import start_coords_2, INVALID_POS, OFFICIAL_NAMES
from cotuong_const import BLACK_PALACE_BOUNDARY, WHITE_PALACE_BOUNDARY
from cotuong_const import MOVE_VERTICALLY_ONE_UNIT_FWD, BOARD_LOC_NUM
from cotuong_const import BLACK_TERRITORY_LOC_NUM, WHITE_TERRITORY_LOC_NUM
from cotuong_const import BLOCKING_TYPES, BLOCKING_RULES
from cotuong_const import board_coor
import pygame

'''
TBD: blocking and eating function => Move to GameState 
'''


class Piece(object):
    def __init__(self, name):
        self.name = name
        self.position = start_coords_2[name]
        self.INVALID_POS = INVALID_POS
        self.id = self.name + '-1'
        self.blocking_rules = self.get_blocking_rules([1])
        self.is_selected = False
        self.moving_list = []
        self.is_alive = True
        self.trans_img = pygame.image.load("Img/transparent.gif")
        self.is_transparent = False
        self.tam = ''
    
    def is_inboard(self, next_pos=INVALID_POS):
        if next_pos != INVALID_POS and 109 >= next_pos >= 11 and next_pos % 10 != 0:
            return True
        elif next_pos == INVALID_POS and 109 >= self.position >= 11 and self.position % 10 != 0:
            return True
        else:
            return False

    def is_in_black_territory(self):
        if 59 >= self.position >= 11 and self.position % 10 != 0:
            return True
        else:
            return False

    def is_in_white_territory(self):
        if 109 >= self.position >= 61 and self.position % 10 != 0:
            return True
        else:
            return False

    def is_in_black_palace(self):
        if self.position in BLACK_PALACE_BOUNDARY:
            return True
        else:
            return False

    def is_in_white_palace(self):
        if self.position in WHITE_PALACE_BOUNDARY:
            return True
        else:
            return False

    def get_blocking_rules(self, rules_id):
        return [BLOCKING_RULES[BLOCKING_TYPES[rule]] for rule in rules_id]

    def valid_move(self, next_pos=INVALID_POS):
        self.position = next_pos
        return self.is_inboard()

    def set_move(self, next_pos):
        return next_pos if self.valid_move(next_pos) else self.position

    def current_state(self):
        return {self.id: self.position}

    def __repr__(self):
        return '{}.id {}: {}'.format(self.name,self.id, self.position)

'''    def calc_moving_path(self, destination_piece, direction_vertical_coordinate, current_vertical_coordinate, direction_parallel_coordinate, direction, border_vertical_coordinate, h_or_v, ignore_color=False):
        if destination_piece != None:
            if destination_piece.name.issuper() == self.name.issuper() or ignore_color:
                for i in range(direction_vertical_coordinate + direction, current_vertical_coordinate, direction):
                    self.__moving_list.append(
                        Point.Point(i, direction_parallel_coordinate) if h_or_v else Point.Point(direction_parallel_coordinate, i))

            else:
                for i in range(direction_vertical_coordinate, current_vertical_coordinate, direction):
                    self.__moving_list.append(
                        Point.Point(i, direction_parallel_coordinate) if h_or_v else Point.Point(direction_parallel_coordinate, i))
        else:
            for i in range(border_vertical_coordinate, current_vertical_coordinate, direction):
                self.__moving_list.append(
                    Point.Point(i, direction_parallel_coordinate) if h_or_v else Point.Point(direction_parallel_coordinate, i))
'''

class Advisor(Piece):
    def __init__(self, name, pos_id=0):
        super().__init__(name)
        if name == 'a':
            self.pos_limit = [14, 16, 25, 34, 36]
            self.img = pygame.image.load("Img/ab.gif",'Img/transparent.gif')
        elif name == 'A':
            self.pos_limit = [104, 106, 95, 84, 86]
            self.img = pygame.image.load("Img/aw.gif",'Img/transparent.gif')
        else:
            raise ValueError('Advisor only takes "a" or "A" for name.')
        self.position = self.position[pos_id]
        self.id = name+str(pos_id)
        self.coor = board_coor[self.position]
        self.col = (self.position % 10) - 1
        self.row = (self.position // 10) - 1
        

    def valid_move(self, next_pos=INVALID_POS):
        if self.position != next_pos and next_pos in self.pos_limit and self.position in self.pos_limit and (self.position + 9 == next_pos or self.position - 9 == next_pos or self.position - 11 == next_pos or self.position + 11 == next_pos):
            return True
        else:
            return False

    

class Cannon(Piece):
    def __init__(self, name, pos_id=0):
        super().__init__(name)
        if name == 'c':
            self.img = pygame.image.load("Img/cb.gif",'Img/transparent.gif')
        elif name == 'C':
            self.img = pygame.image.load("Img/cw.gif",'Img/transparent.gif')
        else:
            raise ValueError('Canon only takes "c" or "C" for name.')
        self.position = self.position[pos_id]
        self.id = name + str(pos_id)
        self.blocking_rules = self.get_blocking_rules([1, 2, 3])
        self.coor = board_coor[self.position]
        self.col = (self.position % 10) - 1
        self.row = (self.position // 10) - 1

    def valid_move(self, next_pos=INVALID_POS):
        if self.position != next_pos and self.is_inboard(self.position) and self.is_inboard(next_pos) and ((abs(next_pos - self.position) <= 8 and (next_pos//10 - self.position//10) == 0) or (abs(next_pos - self.position) >= 10 and abs(next_pos - self.position) % 10 == 0)):
            return True
        else:
            return False  
        
    def setCoor(self, position):
        self.coor = board_coor[position]        

class Elephant(Piece):
    def __init__(self, name, pos_id=0):
        super().__init__(name)
        self.position = self.position[pos_id]
        self.id = name + str(pos_id)
        if name == 'e':
            self.pos_limit = [13, 17, 31, 35, 39, 53, 57]
            self.img = pygame.image.load('Img/eb.gif','Img/transparent.gif')
        elif name == 'E':
            self.img = pygame.image.load('Img/ew.gif','Img/transparent.gif')
            self.pos_limit = [63, 67, 81, 85, 89, 103, 107]
        else:
            raise ValueError("Elephant only takes 'e' or 'E' for name")
        self.blocking_rules = self.get_blocking_rules([1, 4])
        self.coor = board_coor[self.position]
        self.col = (self.position % 10) - 1
        self.row = (self.position // 10) - 1

    def valid_move(self, next_pos=INVALID_POS):
        if self.position != next_pos and next_pos in self.pos_limit and self.position in self.pos_limit and (self.position + 18 == next_pos or self.position - 18 == next_pos or self.position + 22 == next_pos or self.position - 22 == next_pos):
            return True
        else:
            return False

    def setCoor(self, position):
        self.coor = board_coor[position]

class King(Piece):
    def __init__(self, name, pos_id=0):
        super().__init__(name)
        if name == 'k':
            self.pos_limit = BLACK_PALACE_BOUNDARY
            self.img = pygame.image.load('Img/kb.gif','Img/transparent.gif')
        elif name == 'K':
            self.pos_limit = WHITE_PALACE_BOUNDARY
            self.img = pygame.image.load('Img/kw.gif','Img/transparent.gif')
        else:
            raise ValueError('King only takes "k" or "K" for name.')
        self.position = self.position[pos_id]
        self.coor = board_coor[self.position]
        self.id = name + str(pos_id)
        self.col = (self.position % 10) - 1
        self.row = (self.position // 10) - 1

    def valid_move(self, next_pos=INVALID_POS):
        if (self.position != next_pos and next_pos in self.pos_limit and self.position in self.pos_limit and (self.position + 1 == next_pos or self.position - 1 == next_pos or self.position + 10 == next_pos or self.position - 10 == next_pos)):
            return True
        else:
            return False

    def setCoor(self, position):
        self.coor = board_coor[position]

class Horse(Piece):
    def __init__(self, name, pos_id=0):
        super().__init__(name)
        if name == 'h':
            self.img = pygame.image.load("Img/hb.gif",'Img/transparent.gif')
        elif name == 'H':
            self.img = pygame.image.load("Img/hw.gif",'Img/transparent.gif')
        else:
            raise ValueError('Hourse only takes "c" or "C" for name.')
        self.position = self.position[pos_id]
        self.coor = board_coor[self.position]
        self.id = name + str(pos_id)
        self.col = (self.position % 10) - 1
        self.row = (self.position // 10) - 1
        self.blocking_rules = self.get_blocking_rules([1, 6])

    def valid_move(self, next_pos=INVALID_POS):
        if self.position != next_pos and self.is_inboard() and self.is_inboard(next_pos=next_pos) and ((self.position + 8 == next_pos or self.position - 8 == next_pos) or (self.position + 12 == next_pos or self.position - 12 == next_pos) or (self.position + 19 == next_pos or self.position - 19 == next_pos) or (self.position + 21 == next_pos or self.position - 21 == next_pos)):
            return True
        else:
            return False

    def setCoor(self, position):
        self.coor = board_coor[position]

class Pawn(Piece):
    def __init__(self, name, pos_id=0):
        super().__init__(name)
        if name.islower():
            self.fwd_only_pos_limit = [
                i + 10 for i in self.position] + self.position
            self.pos_limit = WHITE_TERRITORY_LOC_NUM + self.fwd_only_pos_limit
        else:
            self.fwd_only_pos_limit = [
                i - 10 for i in self.position] + self.position
            self.pos_limit = BLACK_TERRITORY_LOC_NUM + self.fwd_only_pos_limit
        if name == 'p':
            self.img = pygame.image.load("Img/pb.gif",'Img/transparent.gif')
        elif name == 'P':
            self.img = pygame.image.load("Img/pw.gif",'Img/transparent.gif')
        else:
            raise ValueError('Pawn only takes "c" or "C" for name.')
        self.position = self.position[pos_id]
        self.coor = board_coor[self.position]
        self.id = name + str(pos_id)
        self.col = (self.position % 10) - 1
        self.row = (self.position // 10) - 1

    def valid_move(self, next_pos=INVALID_POS):
        if self.position != next_pos and self.position in self.pos_limit and next_pos in self.pos_limit:
            if self.name.islower() and ((self.is_in_white_territory() and (next_pos - 10 == self.position or next_pos - 1 == self.position or next_pos + 1 == self.position)) or (self.position in self.fwd_only_pos_limit and next_pos - 10 == self.position)):
                return True
            elif self.name.isupper() and ((self.is_in_black_territory() and (next_pos + 10 == self.position or next_pos - 1 == self.position or next_pos + 1 == self.position)) or (self.position in self.fwd_only_pos_limit and next_pos + 10 == self.position)):
                return True
            else:
                return False
        else: return False

    def setCoor(self, position):
        self.coor = board_coor[position]

class Rock(Piece):
    def __init__(self, name, pos_id=0):
        super().__init__(name)
        if name == 'r':
            self.img = pygame.image.load("Img/rb.gif",'Img/transparent.gif')
        elif name == 'R':
            self.img = pygame.image.load("Img/rw.gif",'Img/transparent.gif')
        else:
            raise ValueError('Rock only takes "c" or "C" for name.')
        self.position = self.position[pos_id]
        self.coor = board_coor[self.position]
        self.id = name + str(pos_id)
        self.col = (self.position % 10) - 1
        self.row = (self.position // 10) - 1
        self.blocking_rules = self.get_blocking_rules([1, 2, 3])

    def valid_move(self, next_pos=INVALID_POS):
        if self.position != next_pos and self.is_inboard(self.position) and self.is_inboard(next_pos) and ((abs(next_pos - self.position) <= 8 and (next_pos//10 - self.position//10) == 0) or (abs(next_pos - self.position) >= 10 and abs(next_pos - self.position) % 10 == 0)):
            return True
        else:
            return False

    def setCoor(self, position):
        self.coor = board_coor[position]


"""
import Point


def num_between(max_num, min_num, current):
    return current >= min_num and current <= max_num


def creat_points(list_points, list_vs, list_hs):
    for v in list_vs:
        for h in list_hs:
            list_points.append(Point.Point(v, h))


class Piece(object):

    def __init__(self, name_cn, name, is_red, chessboard):
        self.__name = name
        self.__is_red = is_red
        self.__chessboard = chessboard
        self.__position = Point.Point(None, None)
        self.__moving_list = []
        self.__top = 0
        self.__left = 0
        self.__bottom = 9
        self.__right = 8
        self.__is_alive = True
        self.__name_cn = name_cn

    @property
    def row_num(self):
        return self.__position.y

    @property
    def col_num(self):
        return self.__position.x

    @property
    def is_alive(self):
        return self.__is_alive

    @is_alive.setter
    def is_alive(self, is_alive):
        self.__is_alive = is_alive

    @property
    def chessboard(self):
        return self.__chessboard

    @property
    def is_red(self):
        return self.__is_red

    @property
    def name(self):
        return self.__name

    @property
    def name_cn(self):
        return self.__name_cn

    @property
    def position(self):
        return self.__position

    @property
    def moving_list(self):
        return self.__moving_list

    def clear_moving_list(self):
        self.__moving_list = []

    def add_to_board(self, col_num, row_num):
        if self.border_check(col_num, row_num):
            self.__position.x = col_num
            self.__position.y = row_num
            self.__chessboard.add_chessman(self, col_num, row_num)
        else:
            print("the worng postion")

    def move(self, col_num, row_num):
        if self.in_moving_list(col_num, row_num):
            self.__chessboard.remove_chessman_source(
                self.__position.x, self.__position.y)
            self.__chessboard.update_history(self, col_num, row_num)
            self.__position.x = col_num
            self.__position.y = row_num
            return self.__chessboard.move_chessman(self, col_num, row_num)
        else:
            print("the worng target_position")
            return False

    def in_moving_list(self, col_num, row_num):
        for point in self.__moving_list:
            if point.x == col_num and point.y == row_num:
                return True
        return False

    def calc_moving_list(self):
        pass

    def border_check(self, col_num, row_num):
        return num_between(self.__top, self.__bottom, row_num) and num_between(self.__right, self.__left, col_num)

    def calc_moving_path(self, direction_chessman, direction_vertical_coordinate, current_vertical_coordinate, direction_parallel_coordinate, direction, border_vertical_coordinate, h_or_v, ignore_color=False):
        if direction_chessman != None:
            if direction_chessman.is_red == self.is_red or ignore_color:
                for i in range(direction_vertical_coordinate + direction, current_vertical_coordinate, direction):
                    self.__moving_list.append(
                        Point.Point(i, direction_parallel_coordinate) if h_or_v else Point.Point(direction_parallel_coordinate, i))

            else:
                for i in range(direction_vertical_coordinate, current_vertical_coordinate, direction):
                    self.__moving_list.append(
                        Point.Point(i, direction_parallel_coordinate) if h_or_v else Point.Point(direction_parallel_coordinate, i))
        else:
            for i in range(border_vertical_coordinate, current_vertical_coordinate, direction):
                self.__moving_list.append(
                    Point.Point(i, direction_parallel_coordinate) if h_or_v else Point.Point(direction_parallel_coordinate, i))

    def add_from_probable_points(self, probable_moving_points, current_color):
        for point in probable_moving_points:
            if self.border_check(point.x, point.y):
                chessman = self.chessboard.get_chessman(
                    point.x, point.y)
                if chessman is None or chessman.is_red != current_color:
                    self.moving_list.append(point)


class Rook(Chessman):

    def __init__(self, name_cn, name, is_red, chessboard):
        super(Rook, self).__init__(name_cn, name, is_red, chessboard)
        self._Chessman__top = 9
        self._Chessman__bottom = 0
        self._Chessman__left = 0
        self._Chessman__right = 8

    def calc_moving_list(self):
        current_v_c = super(Rook, self).position.x
        current_h_c = super(Rook, self).position.y
        left = super(Rook, self).chessboard.get_left_first_chessman(
            current_v_c, current_h_c)
        right = super(Rook, self).chessboard.get_right_first_chessman(
            current_v_c, current_h_c)
        top = super(Rook, self).chessboard.get_top_first_chessman(
            current_v_c, current_h_c)
        bottom = super(Rook, self).chessboard.get_bottom_first_chessman(
            current_v_c, current_h_c)

        super(Rook, self).calc_moving_path(left, (left.position.x if left != None else None),
                                           current_v_c, current_h_c, 1, 0, True)
        super(Rook, self).calc_moving_path(right, (right.position.x if right != None else None),
                                           current_v_c, current_h_c, -1, 8, True)
        super(Rook, self).calc_moving_path(top, (top.position.y if top != None else None),
                                           current_h_c, current_v_c, -1, 9, False)
        super(Rook, self).calc_moving_path(bottom, (bottom.position.y if bottom != None else None),
                                           current_h_c, current_v_c, 1, 0, False)


class Knight(Chessman):

    def __init__(self, name_cn, name, is_red, chessboard):
        super(Knight, self).__init__(name_cn, name, is_red, chessboard)
        self._Chessman__top = 9
        self._Chessman__bottom = 0
        self._Chessman__left = 0
        self._Chessman__right = 8

    def calc_moving_list(self):
        current_v_c = super(Knight, self).position.x
        current_h_c = super(Knight, self).position.y
        probable_obstacle_points = []
        probable_moving_points = []
        vs1 = (current_v_c + 1, current_v_c - 1)
        hs1 = (current_h_c,)
        vs2 = (current_v_c,)
        hs2 = (current_h_c + 1, current_h_c - 1)
        creat_points(probable_obstacle_points, vs1, hs1)
        creat_points(probable_obstacle_points, vs2, hs2)
        current_color = super(Knight, self).is_red
        for point in probable_obstacle_points:
            if super(Knight, self).border_check(point.x, point.y):
                chessman = super(Knight, self).chessboard.get_chessman(
                    point.x, point.y)
                if chessman is None:
                    if point.x == current_v_c:
                        probable_moving_points.append(
                            Point.Point(point.x + 1, 2 * point.y - current_h_c))
                        probable_moving_points.append(
                            Point.Point(point.x - 1, 2 * point.y - current_h_c))
                    else:
                        probable_moving_points.append(
                            Point.Point(2 * point.x - current_v_c, point.y + 1))
                        probable_moving_points.append(
                            Point.Point(2 * point.x - current_v_c, point.y - 1))
        super(Knight, self).add_from_probable_points(
            probable_moving_points, current_color)


class Cannon(Chessman):

    def __init__(self, name_cn, name, is_red, chessboard):
        super(Cannon, self).__init__(name_cn, name, is_red, chessboard)
        self._Chessman__top = 9
        self._Chessman__bottom = 0
        self._Chessman__left = 0
        self._Chessman__right = 8

    def calc_moving_list(self):
        current_v_c = super(Cannon, self).position.x
        current_h_c = super(Cannon, self).position.y
        left = super(Cannon, self).chessboard.get_left_first_chessman(
            current_v_c, current_h_c)
        right = super(Cannon, self).chessboard.get_right_first_chessman(
            current_v_c, current_h_c)
        top = super(Cannon, self).chessboard.get_top_first_chessman(
            current_v_c, current_h_c)
        bottom = super(Cannon, self).chessboard.get_bottom_first_chessman(
            current_v_c, current_h_c)
        tar_left = super(Cannon, self).chessboard.get_left_second_chessman(
            current_v_c, current_h_c)
        tar_right = super(Cannon, self).chessboard.get_right_second_chessman(
            current_v_c, current_h_c)
        tar_top = super(Cannon, self).chessboard.get_top_second_chessman(
            current_v_c, current_h_c)
        tar_bottom = super(Cannon, self).chessboard.get_bottom_second_chessman(
            current_v_c, current_h_c)
        super(Cannon, self).calc_moving_path(left, (left.position.x if left != None else None),
                                             current_v_c, current_h_c, 1, 0, True, True)
        super(Cannon, self).calc_moving_path(right, (right.position.x if right != None else None),
                                             current_v_c, current_h_c, -1, 8, True, True)
        super(Cannon, self).calc_moving_path(top, (top.position.y if top != None else None),
                                             current_h_c, current_v_c, -1, 9, False, True)
        super(Cannon, self).calc_moving_path(bottom, (bottom.position.y if bottom != None else None),
                                             current_h_c, current_v_c, 1, 0, False, True)
        current_color = super(Cannon, self).is_red
        if tar_left != None and tar_left.is_red != current_color:
            super(Cannon, self).moving_list.append(
                Point.Point(tar_left.position.x, tar_left.position.y))
        if tar_right != None and tar_right.is_red != current_color:
            super(Cannon, self).moving_list.append(
                Point.Point(tar_right.position.x, tar_right.position.y))
        if tar_top != None and tar_top.is_red != current_color:
            super(Cannon, self).moving_list.append(
                Point.Point(tar_top.position.x, tar_top.position.y))
        if tar_bottom != None and tar_bottom.is_red != current_color:
            super(Cannon, self).moving_list.append(
                Point.Point(tar_bottom.position.x, tar_bottom.position.y))


class Mandarin(Chessman):

    def __init__(self, name_cn, name, is_red, chessboard):
        super(Mandarin, self).__init__(name_cn, name, is_red, chessboard)
        if self.is_red:
            self._Chessman__top = 2
            self._Chessman__bottom = 0
            self._Chessman__left = 3
            self._Chessman__right = 5
        else:
            self._Chessman__top = 9
            self._Chessman__bottom = 7
            self._Chessman__left = 3
            self._Chessman__right = 5

    def calc_moving_list(self):
        current_v_c = super(Mandarin, self).position.x
        current_h_c = super(Mandarin, self).position.y
        probable_moving_points = []
        vs1 = (current_v_c + 1, current_v_c - 1)
        hs1 = (current_h_c + 1, current_h_c - 1)
        creat_points(probable_moving_points, vs1, hs1)
        current_color = super(Mandarin, self).is_red

        super(Mandarin, self).add_from_probable_points(
            probable_moving_points, current_color)


class Elephant(Chessman):

    def __init__(self, name_cn, name, is_red, chessboard):
        super(Elephant, self).__init__(name_cn, name, is_red, chessboard)
        if self.is_red:
            self._Chessman__top = 4
            self._Chessman__bottom = 0
            self._Chessman__left = 0
            self._Chessman__right = 8
        else:
            self._Chessman__top = 9
            self._Chessman__bottom = 5
            self._Chessman__left = 0
            self._Chessman__right = 8

    def calc_moving_list(self):
        current_v_c = super(Elephant, self).position.x
        current_h_c = super(Elephant, self).position.y
        probable_obstacle_points = []
        probable_moving_points = []
        vs1 = (current_v_c + 1, current_v_c - 1)
        hs1 = (current_h_c + 1, current_h_c - 1)
        creat_points(probable_obstacle_points, vs1, hs1)
        current_color = super(Elephant, self).is_red
        for point in probable_obstacle_points:
            if super(Elephant, self).border_check(point.x, point.y):
                chessman = super(Elephant, self).chessboard.get_chessman(
                    point.x, point.y)
                if chessman is None:
                    probable_moving_points.append(
                        Point.Point(2 * point.x - current_v_c, 2 * point.y - current_h_c))
        super(Elephant, self).add_from_probable_points(
            probable_moving_points, current_color)


class Pawn(Chessman):

    def __init__(self, name_cn, name, is_red, chessboard):
        super(Pawn, self).__init__(name_cn, name, is_red, chessboard)
        if self.is_red:
            self._Chessman__top = 9
            self._Chessman__bottom = 3
            self._Chessman__left = 0
            self._Chessman__right = 8
            self.__direction = 1
            self.__river = 5
        else:
            self._Chessman__top = 6
            self._Chessman__bottom = 0
            self._Chessman__left = 0
            self._Chessman__right = 8
            self.__direction = -1
            self.__river = 4

    def calc_moving_list(self):
        current_v_c = super(Pawn, self).position.x
        current_h_c = super(Pawn, self).position.y
        probable_moving_points = []
        current_color = super(Pawn, self).is_red
        probable_moving_points.append(
            Point.Point(current_v_c, current_h_c + self.__direction))
        if current_h_c * self.__direction >= self.__river * self.__direction:
            probable_moving_points.append(
                Point.Point(current_v_c + 1, current_h_c))
            probable_moving_points.append(
                Point.Point(current_v_c - 1, current_h_c))
        super(Pawn, self).add_from_probable_points(
            probable_moving_points, current_color)


class King(Chessman):

    def __init__(self, name_cn, name, is_red, chessboard):
        super(King, self).__init__(name_cn, name, is_red, chessboard)
        if self.is_red:
            self._Chessman__top = 2
            self._Chessman__bottom = 0
            self._Chessman__left = 3
            self._Chessman__right = 5
        else:
            self._Chessman__top = 9
            self._Chessman__bottom = 7
            self._Chessman__left = 3
            self._Chessman__right = 5

    def calc_moving_list(self):
        current_v_c = super(King, self).position.x
        current_h_c = super(King, self).position.y
        probable_moving_points = []
        vs1 = (current_v_c + 1, current_v_c - 1)
        hs1 = (current_h_c,)
        vs2 = (current_v_c,)
        hs2 = (current_h_c + 1, current_h_c - 1)
        creat_points(probable_moving_points, vs1, hs1)
        creat_points(probable_moving_points, vs2, hs2)
        current_color = super(King, self).is_red
        super(King, self).add_from_probable_points(
            probable_moving_points, current_color)
"""