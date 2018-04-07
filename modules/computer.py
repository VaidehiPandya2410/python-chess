from board import *

def matrix_to_tuple(array, empty_array):
    """
    Given a 2D list, converts it to 2D tuple. This is useful for using a
    matrix as a key in a dictionary
    (an empty 8x8 should be given, just for efficiency)
    """
    for i in range(8):
        empty_array[i] = tuple(array[i])
    return tuple(empty_array)

# possible improvement: Make a list of all the pieces, so you don't have
# to iterate through the whole board for move gen
def move_gen(board, color):
    """
    Generates the legal moves from a board state, for a specific color
    Return: moves (dict) - maps coord (y,x) to a set containing the coords of
            where is can legally move
    """
    moves = dict()
    # Generates all the legal moves and stores them in whitemoves, blackmoves
    for j in range(8):
        for i in range(8):
            piece = board.array[i][j]
            if piece != None and piece.color == color:
                legal_moves = piece.gen_legal_moves(board)
                if legal_moves:
                    moves[(i,j)] = legal_moves
    return moves

def minimax(board, depth, alpha, beta, maximizing, memo):
    """
    Minimax algorithm with alpha-beta pruning determines the best move for
    black from the current board state.
    Return: bestValue - score of the board resulting from the best move
            move - tuple containing the start coord and the end coord of the best move
            ex. ((y1,x1),(y2,x2)) -> the piece at (y1,x1) should move to (y2,x2)
    """

    tuple_mat = matrix_to_tuple(board.array, board.empty)
    if tuple_mat in memo:
        return memo[tuple_mat], 0

    if depth == 0: # end of the search is reached
        memo[tuple_mat] = board.score
        return board.score, 0

    if maximizing:
        bestValue = float("-inf")
        black_moves = move_gen(board,"b")
        for start, move_set in black_moves.items():
            for end in move_set:

                #develop the 'child'
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece,end[0],end[1])
                #change the board score
                if dest != None:
                    board.score += board.pvalue_dict[type(dest)]

                v, __ = minimax(board, depth - 1,alpha,beta, False, memo)
                bestValue = max(bestValue, v)
                alpha = max(alpha, bestValue)

                # revert the board
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1])
                board.array[end[0]][end[1]] = dest
                move = (start, (end[0],end[1])) # preserve the move

                #revert the score
                if dest != None:
                    board.score -= board.pvalue_dict[type(dest)]

                if beta <= alpha:
                    return bestValue, move

        return bestValue, move

    else:    #(* minimizing player *)
        bestValue = float("inf")
        white_moves = move_gen(board,"w")
        for start, move_set in white_moves.items():
            for end in move_set:

                #DEVELOP the child
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece,end[0],end[1])

                #update the score
                if dest != None:
                    board.score -= board.pvalue_dict[type(dest)]

                v, __ = minimax(board, depth - 1,alpha,beta, True, memo)
                bestValue = min(v, bestValue)
                beta = min(beta,bestValue)

                #preserve shit
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1])
                board.array[end[0]][end[1]] = dest

                # revert the score
                if dest != None:
                    board.score += board.pvalue_dict[type(dest)]

                if beta <= alpha:
                    return bestValue, 0

        return bestValue, 0


b = Board()

b.array[2][1] = Pawn("w",2,1)
b.array[2][6] = Rook("w",2,6)

b.array[6][0] = None
b.array[7][7] = None

trans_table = dict()
value, move = minimax(b,5,float("-inf"),float("inf"), True, trans_table)
print(len(trans_table))
print(" ")
b.print_to_terminal()
print(value)
print(move)