from ex11_backtrack import general_backtracking


def print_board(board, board_size=9):
    """ prints a sudoku board to the screen

    ---  board should be implemented as a dictinary 
         that points from a location to a number {(row,col):num}
    """
    for row in range(board_size):
        if (row % 3 == 0):
            print('-------------')
        toPrint = ''
        for col in range(board_size):
            if (col % 3 == 0):
                toPrint += '|'
            toPrint += str(board[(row, col)])
        toPrint += '|'
        print(toPrint)
    print('-------------')


### to implement
def load_game(sudoku_file):
    '''A function that load the board game to a useable dic of cords and vule
    :param 01
           12
    :return(0,0):0,(0,1):1,(1,0):1,(1,1):2'''
    dic = {}
    count = 0
    sudoku_file=open(sudoku_file)
    for line in sudoku_file:
        line = line.rstrip().replace(',', '')
        for num in range(len(line)):
            tup = (count, num)
            dic[tup] = int(line[num])
        count += 1
    sudoku_file.close()
    return dic


def sudoku_squre(cord):
    '''A function that get a cord from the sudoku bord and return all the
    cords that are in the same squre of the 9X9 sudoku'''
    list_sqr = []
    col_inter = (cord[0] // 3) * 3
    row_inter = (cord[1] // 3) * 3
    for i in range(3):
        for j in range(3):
            list_sqr.append((col_inter + i, row_inter + j))
    list_sqr.remove(cord)
    return list_sqr


def check_board(board, x,*args):
    '''A function that gets a board mean a dict of all the cords in the sudkou table a spcipic cord and
    a number the function return True if it is legal assignment and false if not'''
    row = [tups for tups in board if tups[0] == x[0] ]
    row.remove(x)
    col = [tups for tups in board if tups[1] == x[1] ]
    col.remove(x)
    sqr = sudoku_squre(x)
    no_cords=set(row+col+sqr)
    for cord in no_cords:
        if board[cord]==args[0]:
            return False
    return True



def run_game(sudoku_file, print_mode=False):
    '''A function that use the general_backtracking function to soulve the sudouko table
    :return true if the table is solvable and print the board if so
    the function will and False if the table is unsolvable'''
    board=load_game(sudoku_file)
    set_of_ass = []
    for i in range(1, 10):
        set_of_ass.append(i)
    list_of_items=[i for i in board if board[i]==0]
    list_of_items.sort()
    if general_backtracking(list_of_items,board,0,set_of_ass,check_board):
        print_mode=True
    if print_mode==True:
        print_board(board)
        return True
    return False


