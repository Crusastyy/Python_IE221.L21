WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)

w = 'w'
b = 'b'
advisor = 'a'
cannon = 'c'
elephant = 'e'
king = 'k'
horse = 'h'
pawn = 'p'
rock = 'r'

OFFICIAL_NAMES = {
    'a': 'Advisor', 
    'c': 'Cannon', 
    'e': 'Elephant', 
    'k': 'King',
    'h': 'Horse',
    'p': 'Pawn',
    'r': 'Rock'
}

DESTINATION = 'destination'
VERTICAL = 'vertical'
HORIZONTAL = 'horizontal'
DIAGONAL_LEFT_DESC = 'diagonal_left_descend_to_right'
DIAGONAL_LEFT_ASCE = 'diagonal_right_ascend_to_right'
LSHAPE = 'lshape'
BLOCKING_TYPES = {
    1: DESTINATION,
    2: VERTICAL,
    3: HORIZONTAL,
    4: DIAGONAL_LEFT_DESC,
    5: DIAGONAL_LEFT_ASCE,
    6: LSHAPE
}
BLOCKING_RULES = {
    DESTINATION: lambda curr_pos, target_pos: [target_pos], 
    VERTICAL: lambda curr_pos, target_pos: list(range(curr_pos + 10, target_pos - 1, 10)) if target_pos > curr_pos else list(range(target_pos + 10, curr_pos - 1, 10)),
    HORIZONTAL: lambda curr_pos, target_pos: list(range(curr_pos + 1, target_pos)) if ((target_pos > curr_pos) and (target_pos-curr_pos < 9)) else (list(range(target_pos + 1, curr_pos)) if ((target_pos < curr_pos) and (-target_pos+curr_pos < 9)) else list(range(1,0))),
    DIAGONAL_LEFT_DESC: lambda curr_pos, target_pos: [curr_pos - 11] if curr_pos - 22 == target_pos else ([curr_pos - 9] if curr_pos - 18 == target_pos else ([curr_pos + 11] if target_pos - curr_pos == 22 else [curr_pos + 9])),
    DIAGONAL_LEFT_ASCE: lambda curr_pos, target_pos: [],
    LSHAPE: lambda curr_pos, target_pos: [curr_pos + 10] if target_pos - curr_pos >= 19 else ([curr_pos - 10] if curr_pos - target_pos >= 19 else ([curr_pos - 1] if ((curr_pos - 12 == target_pos) or (curr_pos + 8 == target_pos)) else ([curr_pos + 1] if ((curr_pos - 8 == target_pos) or (curr_pos + 12 == target_pos)) else [])))
}

INVALID_POS = -1110

start_coords = {
    w: {
        advisor: [104, 106],
        cannon: [82, 88],
        elephant: [103, 107],
        king: [105],
        horse: [102, 108],
        pawn: [71, 73, 75, 77, 79],
        rock: [101, 109]
    },
    b: {
        advisor: [14, 16],
        cannon: [32, 38],
        elephant: [13, 17],
        king: [15],
        horse: [12, 18],
        pawn: [41, 43, 45, 47, 49],
        rock: [11, 19]
    }
}

start_coords_2 = {
    'A': [104, 106],
    'C': [82, 88],
    'E': [103, 107],
    'K': [105],
    'H': [102, 108],
    'P': [71, 73, 75, 77, 79],
    'R': [101, 109],
    'a': [14, 16],
    'c': [32, 38],
    'e': [13, 17],
    'k': [15],
    'h': [12, 18],
    'p': [41, 43, 45, 47, 49],
    'r': [11, 19]
}

board_matrix = [
    [0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10],
    [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 110],
    [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 210],
    [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 310],
    [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 410],
    [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 510],
    [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 610],
    [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 710],
    [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 810],
    [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 910],
    [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 1010],
    [110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 1110]
]

BOARD_LOC_NUM = [i for i in range(11, 110) if i % 10 != 0]
WHITE_TERRITORY_LOC_NUM = [i for i in BOARD_LOC_NUM if i>= 61]
BLACK_TERRITORY_LOC_NUM = [i for i in BOARD_LOC_NUM if i<= 59]

BLACK_PALACE_BOUNDARY = [14, 15, 16, 24, 25, 26, 34, 35, 36]
WHITE_PALACE_BOUNDARY = [84, 85, 86, 94, 95, 96, 104, 105, 106]

MOVE_VERTICALLY_ONE_UNIT_FWD = {w: -10, b: 10}
MOVE_VERTICALLY_ONE_UNIT_BWD = {w: 10, b: -10}
MOVE_HORIZONTALLY_ONE_UNIT_LEFT = {w: -1, b: 1}
MOVE_HORIZONTALLY_ONE_UNIT_RIGHT = {w: 1, b: -1}


board_coor = {
    11: [40, 40],	12: [120, 38],      13: [200, 38],      14: [280, 38],	    15: [360, 38],      16: [440, 38],      17: [520, 38],	    18: [600, 38],      19: [680, 38],
    21: [40, 120],  22: [120, 118],	    23: [200, 118],	    24: [280, 118],	    25: [360, 118],	    26: [440, 118],	    27: [520, 118],	    28: [600, 118],	    29: [680, 118],
    31: [40, 200],  32: [120, 198],	    33: [200, 198],	    34: [280, 198],	    35: [360, 198],	    36: [440, 198],	    37: [520, 198],	    38: [600, 198],	    39: [680, 198],
    41: [40, 280],	42: [120, 278],	    43: [200, 278],	    44: [280, 278],	    45: [360, 278],	    46: [440, 278],	    47: [520, 278],	    48: [600, 278],	    49: [680, 278],
    51: [40, 360],	52: [120, 358],	    53: [200, 358],	    54: [280, 358],	    55: [360, 358],	    56: [440, 358],	    57: [520, 358],	    58: [600, 358],	    59: [680, 358],
    61: [40, 440],	62: [120, 439],	    63: [200, 439],	    64: [280, 439],	    65: [360, 439],	    66: [440, 439],	    67: [520, 439],	    68: [600, 439],	    69: [680, 439],
    71: [40, 520],	72: [120, 519],	    73: [200, 519],	    74: [280, 519],	    75: [360, 519],	    76: [440, 519],	    77: [520, 519],	    78: [600, 519],	    79: [680, 519],
    81: [40, 600],	82: [120, 599],	    83: [200, 599],	    84: [280, 599],	    85: [360, 599],	    86: [440, 599],	    87: [520, 599],	    88: [600, 599],	    89: [680, 599],
    91: [40, 680],	92: [120, 679],	    93: [200, 679],	    94: [280, 679],	    95: [360, 679],	    96: [440, 679],	    97: [520, 679],	    98: [600, 679],	    99: [680, 679],
    101: [40, 760],	102: [120, 759],	103: [200, 759],	104: [280, 759],	105: [360, 759],	106: [440, 759],	107: [520, 759],	108: [600, 759],	109: [680, 759]
}

location_chess= [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]