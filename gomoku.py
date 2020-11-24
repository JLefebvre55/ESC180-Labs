"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""

def is_empty(board):
    '''
    Checks if all entries in board `board` are empty, i.e. equal to " ".
    '''
    for row in board:
        for entry in row:
            if(entry != " "):
                return False
    return True

#3 long, ends at (6,1), direction (1,0), OPEN
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''
    Checks the bounded-ness of a VALID, COMPLETE sequence ending at (`y_end`, `x_end`) with direction (`d_y`, `d_x`) on board `board`.
    \n
    Returns "OPEN", "SEMIOPEN", or "CLOSED" to indicate bounded-ness.
    '''
    x_start = x_end - (length-1)*d_x    #1-2*0 = 1
    y_start = y_end - (length-1)*d_y    #6-2*1 = 4
    
    bounded_ends = 0
    #Start end
    if (d_y != 0 and y_start == 0) or (d_x != 0 and x_start == 0) or (d_x == -1 and x_start == len(board[0])-1) or board[y_start-d_y][x_start-d_x] != " ":  #board[4-1 = 3][1-0 = 1] == " "
        bounded_ends+=1
    #End end
    if (d_y != 0 and y_end == len(board)-1) or ((d_x == 1 and x_end == len(board[0])-1) or (d_x == -1 and x_end == 0)) or board[y_end+d_y][x_end+d_x] != " ":  #board[6+1 = 7][1+0 = 1] == " "
        bounded_ends+=1
    
    if bounded_ends == 0:
        return "OPEN"
    if bounded_ends == 1:
        return "SEMIOPEN"
    if bounded_ends == 2:
        return "CLOSED"
    
def row_length(board, y_start, x_start, d_y, d_x):
    '''
    Gets the length of the "row" starting at EDGE POSITION (`y_start`, `x_start`) along (`d_y`, `d_x`) on board `board`.
    \n
    Assumes `d_y` and `d_x` are both in `[-1, 0, 1]`
    '''
    if d_x == 0:
        return len(board)
    if d_y == 0:
        return len(board[0])
    if d_x == -1:
        return min(len(board)-y_start, x_start+1)
    else:
        return min(len(board[0]) - x_start, len(board) - y_start)
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x, closed_seq = False):
    L = 0
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0
    RL = row_length(board, y_start, x_start, d_y, d_x)
    for i in range(RL):
        if board[y_start + i*d_y][x_start + i*d_x] == col:
            L += 1
            if L > length:
                continue
            if L == length:
                # if (y_start + i*d_y == len(board)-1 or x_start + i*d_x == len(board[0])-1 or board[y_start + (i+1)*d_y][x_start + (i+1)*d_x] != col):#Length match found ONLY if at end of board OR next space empty
                if i == RL - 1 or board[y_start + (i+1)*d_y][x_start + (i+1)*d_x] != col:
                    boundedness = is_bounded(board, y_start + i*d_y, x_start + i*d_x, L, d_y, d_x)
                    if(boundedness == "OPEN"):
                        open_seq_count += 1
                    elif(boundedness == "SEMIOPEN"):
                        semi_open_seq_count += 1
                    elif(boundedness == "CLOSED"):
                        closed_seq_count += 1
        else: #Escaped sequence -> Reset
            L = 0
    if(closed_seq):
        return open_seq_count, semi_open_seq_count, closed_seq_count
    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length, closed_seq = False):
    open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0
    
    #HORIZONTAL - d_y = 0, d_x = 1
    for row in range(len(board)):
        a, b, c = detect_row(board, col, row, 0, length, 0, 1, True)
        open_seq_count += a
        semi_open_seq_count += b
        closed_seq_count += c
        
    #VERTICAL - d_y = 1, d_x = 0
    for column in range(len(board[0])):
        a, b, c = detect_row(board, col, 0, column, length, 1, 0, True)
        open_seq_count += a
        semi_open_seq_count += b
        closed_seq_count += c

    #LEFT-RIGHT DIAGONAL, TOP-RIGHT CORNER - d_y = 1, d_x = 1 - x-pivot 0->flush
    for pivot in range(len(board[0])-length+1):
        a, b, c = detect_row(board, col, 0, pivot, length, 1, 1, True)
        open_seq_count += a
        semi_open_seq_count += b
        closed_seq_count += c
        
    #LEFT-RIGHT DIAGONAL, BOTTOM-LEFT CORNER - d_y = 1, d_x = 1 - y-pivot 1->flush
    for pivot in range(1, len(board[0])-length+1):
        a, b, c = detect_row(board, col, pivot, 0, length, 1, 1, True)
        open_seq_count += a
        semi_open_seq_count += b
        closed_seq_count += c
    
    #RIGHT-LEFT DIAGONAL, TOP-LEFT CORNER - d_y = 1, d_x = -1 - x-pivot starting at flush->end
    for pivot in range(length-1, len(board[0])):
        a, b, c = detect_row(board, col, 0, pivot, length, 1, -1, True)
        open_seq_count += a
        semi_open_seq_count += b
        closed_seq_count += c
        
    #RIGHT-LEFT DIAGONAL, BOTTOM-RIGHT CORNER - d_y = 1, d_x = -1 - y-pivot starting at half->flush
    for pivot in range(1, len(board)-length+1):
        a, b, c = detect_row(board, col, pivot, len(board[0])-1, length, 1, -1, True)
        open_seq_count += a
        semi_open_seq_count += b
        closed_seq_count += c
    
    if closed_seq:
        return open_seq_count, semi_open_seq_count, closed_seq_count
    return open_seq_count, semi_open_seq_count
    
def get_empty(board):
    L = []
    for row in range(len(board)):
        for entry in range(len(board[row])):
            if board[row][entry] == " ":
                L.append((row, entry))
    return L

def get_first_empty(board):
    for row in range(len(board)):
        for entry in range(len(board[row])):
            if board[row][entry] == " ":
                return (row, entry)

def get_top_N(board):
    moves = [{
        "move" : get_first_empty(board),
        "score" : -1
    },]
    for move in get_empty(board):
        temp = board[move[0]][move[1]]
        board[move[0]][move[1]] = "b"   #Place piece
        newscore = score(board)
        
        #If greater than the lowest top-N score, insert sorted and remove the lowest
        if newscore > moves[-1]["score"]:
            for i in range(len(moves)): 
                if newscore > moves[i]["score"]: 
                    moves.insert(i, {
                        "move" : move,
                        "score" : newscore
                    })
                    if(len(moves) > CHECK_TOP):
                        moves.pop()
                    break
        board[move[0]][move[1]] = temp
    return moves
            
MAX_DEPTH = 2   #Recursion depth
CHECK_TOP = 4   #Perform recursion on the top N contenders
def sum_score_tree(board, depth=0):
    # Get shallow-scored top-N
    # Recurse with each of top-N placed on newboard
    
    moves = get_top_N(board)
    
    if(depth < MAX_DEPTH):
        for move in moves:
            temp = board[move["move"][0]][move["move"][1]]
            board[move["move"][0]][move["move"][1]] = "b"
            move["score"] += sum_score_tree(board, depth+1)
            board[move["move"][0]][move["move"][1]] = temp
    return sum([m["score"] for m in moves])
            
def search_max(board):
    bestmove = {
        "move" : get_first_empty(board),
        "score" : -1
    }
    for move in get_top_N(board):
        temp = board[move["move"][0]][move["move"][1]]
        board[move["move"][0]][move["move"][1]] = "b"
        move["score"] += sum_score_tree(board)
        board[move["move"][0]][move["move"][1]] = temp
        if(move["score"] > bestmove["score"]):
            bestmove = move
    return bestmove["move"]
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
    b = detect_rows(board, "b", 5, True)
    w = detect_rows(board, "w", 5, True)
    if any([n >= 1 for n in b]):
        return "Black won"
    if any([n >= 1 for n in w]):
        return "White won"
    if len(get_empty(board)) == 0:
        return "Draw"
    return "Continue playing"
        

def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
            
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0 
                 
if __name__ == '__main__':
    print(play_gomoku(8))
    