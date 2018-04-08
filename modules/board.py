from modules.pieces import *


class Board:
    """
    Board is represented by an 8x8 array. 'None' indicates an empty square.
    """

    def __init__(self):
        self.empty = [[None for x in range(8)] for y in range(8)]
        self.black_king = King("b", 0, 4)
        self.white_king = King("w", 7, 4)
        self.array = [
            [Rook("b", 0, 0), Knight("b", 0, 1), Bishop("b", 0, 2), Queen("b", 0, 3),
                self.black_king, Bishop("b", 0, 5), Knight("b", 0, 6), Rook("b", 0, 7)],
            [Pawn("b", 1, i) for i in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [Pawn("w", 6, i) for i in range(8)],
            [Rook("w", 7, 0), Knight("w", 7, 1), Bishop("w", 7, 2), Queen("w", 7, 3),
                self.white_king, Bishop("w", 7, 5), Knight("w", 7, 6), Rook("w", 7, 7)]
        ]
        # used in minimax to find the best move
        self.score = 0
        # maps piecetype to relative value
        self.pvalue_dict = {King: 200, Queen: 9,
                            Rook: 5, Knight: 3, Bishop: 3, Pawn: 1}

    def move_piece(self, piece, y, x):
        """
        Moves an instance of the piece class to (y,x)
        """
        oldx = piece.x
        oldy = piece.y
        piece.x = x
        piece.y = y
        piece.rect.x = x*60
        piece.rect.y = y*60
        self.array[oldy][oldx] = None
        self.array[y][x] = piece

    """ NOT VALID W/ CURRENT BOARD IMPLEMENTATION
    # this is not a good place for this function, testing stuff out
    # Determine if there's a check on the king of the color inputted
    def determine_check(self, color, kingy, kingx):
        flag = False
        if color == "w":
            for __, attacked in self.blackmoves.items():
                if (kingy, kingx) in attacked:
                    flag = True
        elif color == "b":
            for __, attacked in self.whitemoves.items():
                if (kingy, kingx) in attacked:
                    flag = True
        return flag
    """

    def print_to_terminal(self):
        """
        Prints the board to the terminal
        """
        for j in range(8):
            arr = []
            for piece in self.array[j]:
                if piece != None:
                    arr.append(piece.color + piece.symbol)
                else:
                    arr.append("--")
            print(arr)
