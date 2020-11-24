'''
 X | O | X
---+---+---
 O | O | X    
---+---+---
   | X | 
'''

import random
import copy

# SETUP

def print_board_and_legend(board):
    '''
    Print the current board `board` next to the placement legend.
    '''
    for i in range(3):
        line1 = " " +  board[i][0] + " | " + board[i][1] + " | " +  board[i][2]
        line2 = "  " + str(3*i+1)  + " | " + str(3*i+2)  + " | " +  str(3*i+3) 
        print(line1 + " "*5 + line2)
        if i < 2:
            print("---+---+---" + " "*5 + "---+---+---")
        
def make_empty_board():
    '''
    Create and return a new 3x3 tic tac toe board.
    '''
    board = []
    for i in range(3):
        board.append([" "]*3)
    return board

# PROBLEM 1
def get_board_coord(square_num):
    '''
    Get the board coordinates (2-list) for a user input `square_num`
    '''
    if(square_num < 1 or square_num > 9):
        raise ValueError("Board position must be between 1 and 9.")
    return [((square_num - 1) // 3), (square_num-1) % 3]

def put_in_board(board, mark, square_num):
    '''
    Puts a mark `mark` in a position based on user input
    '''
    
    coord = get_board_coord(square_num)
    
    board[coord[0]][coord[1]] = mark
    
#OLD USER INPUT LOOP FOR PROBLEM 1

def get_user_input(board):
    mark = "O"
    count = 0
    while count < 9:
        print_board_and_legend(board)
        
        mark = "X" if mark == "O" else "O"
        
        #Which position?
        move = -1
        while move < 1 or move > 9:
            try:
                move = int(input("("+mark+") Enter your move: "))
            except:
                continue
        put_in_board(board, mark, move)
        count +=1
    
#PROBLEM 2

def get_free_squares(board):
    '''
    Get the list of all the free positions (2-list) on board `board`.
    '''
    free_squares = []
    for row in range(3):
        for spot in range(3):
            if board[row][spot] != "X" and board[row][spot] != "O":
                free_squares.append([row, spot])
    return free_squares

def make_random_move(board, mark):
    '''
    Make a random move `mark` in a free square on board `board`.
    '''
    free_squares = get_free_squares(board)
    move = free_squares[int(len(free_squares) * random.random())]
    board[move[0]][move[1]] = mark
    
def is_empty(board, move):
    '''
    Check to see if the position `move` (2-list) on board `board` has neither an "X" or an "O" in it.
    '''
    coord = get_board_coord(move)
    return board[coord[0]][coord[1]] != "X" and board[coord[0]][coord[1]] != "O"
    
#OLD USER INPUT LOOP FOR PROBLEM 2

# def get_user_input(board):
#     count = 0
#     while count < 9:
#         print_board_and_legend(board)
#         move = -1
#         while move < 1 or move > 9 or not is_empty(board, move):
#             try:
#                 move = int(input("(X) Enter your move: "))
#             except:
#                 print("")
#                 continue
#         put_in_board(board, "X", move)
#         print_board_and_legend(board)
#         make_random_move(board, "O")
#         count += 2

#PROBLEM 3
def is_row_all_marks(board, row_i, mark):
    '''
    Check to see if all entries in row `row_i` of board `board` are mark `mark`
    '''
    for spot in board[row_i]:
        if spot != mark:
            return False
    return True

def is_col_all_marks(board, col_i, mark):
    '''
    Check to see if all entries in column `col_i` of board `board` are mark `mark`
    '''
    for row in range(3):
        if board[row][col_i] != mark:
            return False
    return True

def is_win(board, mark):
    '''
    Check to see if player designated by mark `mark` has won the game on the board `board`.
    '''
    for row in range(3):
        if is_row_all_marks(board, row, mark):
            return True
    for col in range(3):
        if is_col_all_marks(board, col, mark):
            return True
    if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
        return True
    if board[0][2] == mark and board[1][1] == mark and board[2][0] == mark:
        return True
    return False

def get_user_input(board):
    '''
    Print the current board and input legend, get valid (blank, 1<=x<=9) user "X" input, and make the move on board `board`.
    '''
    print_board_and_legend(board)
    move = -1
    while move < 1 or move > 9 or not is_empty(board, move):
        try:
            move = int(input("(X) Enter your move: "))
        except:
            print("")
            continue
    put_in_board(board, "X", move)
    
def make_smartest_move_Os(board):
    '''
    Make a smart move for "O"s on board `board`.
    1) Check to see if an immediate win is possible for "O"; if so, take that position.
    2) Check to see if an immediate win is possible for "X"; if so, take that position.
    3) Place randomly.
    '''
    free_squares = get_free_squares(board)
    
    #IMMEDIATE OFFENSE
    for move in free_squares:
        newboard = copy.deepcopy(board)
        newboard[move[0]][move[1]] = "O"
        if is_win(newboard, "O"):
            board[move[0]][move[1]] = "O"
            return
    
    #DEFENSE
    for move in free_squares:
        newboard = copy.deepcopy(board)
        newboard[move[0]][move[1]] = "X"
        if is_win(newboard, "X"):
            board[move[0]][move[1]] = "O"
            return
    
    make_random_move(board, "O")
    
if __name__ == '__main__':
    board = make_empty_board()
    winner = None
    moves = 0
    
    while moves < 9:
        get_user_input(board)
        moves +=1
        if(is_win(board, "X")):
            winner = "X"
            break;
        if(moves > 9):
            break;
        
        make_smartest_move_Os(board)
        
        moves +=1
        if(is_win(board, "O")):
            winner = "O"
            break;
        
    print_board_and_legend(board)
    if(winner):
        print(winner, "wins!")
    else:
        print("Tie!")         