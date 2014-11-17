# Sudoko a-star example
from copy import deepcopy

Grid = [['4', '.', '7',     '3', '.', '9',      '8', '.', '5'],
        ['.', '3', '.',     '.', '.', '.',      '.', '.', '.'],
        ['.', '.', '.',     '7', '.', '.',      '.', '.', '.'],
        
        ['.', '2', '.',     '.', '.', '.',      '.', '6', '.'],
        ['.', '.', '.',     '.', '8', '.',      '4', '.', '.'],
        ['.', '.', '.',     '.', '1', '.',      '.', '.', '.'],

        ['.', '.', '.',     '6', '.', '3',      '.', '7', '.'],
        ['5', '.', '.',     '2', '.', '.',      '.', '.', '.'],
        ['1', '.', '4',     '.', '.', '.',      '.', '.', '.']]

square_indx = [[(0,3),(0,3)],
               [(0,3),(3,6)],
               [(0,3),(6,9)],
               
               [(3,6),(0,3)],
               [(3,6),(3,6)],
               [(3,6),(6,9)],
               
               [(6,9),(0,3)],
               [(6,9),(3,6)],
               [(6,9),(6,9)]]

elements = ['1','2','3','4','5','6','7','8','9']

def get_squares(new_Grid):
    squares = []
    for i in range(0,9):
        square = {}
        for x in range(square_indx[i][0][0],square_indx[i][0][1]):
            for y in range(square_indx[i][1][0],square_indx[i][1][1]):
                square[(x,y)] = new_Grid[x][y]
        squares.append(square)
    return squares

def get_rows(new_Grid):
    rows = []
    for i in range(0,9):
        row = {}
        for y in range(0,9):
            row[(i,y)] = new_Grid[i][y]
        rows.append(row)
    return rows

def get_cols(new_Grid):
    cols = []
    for i in range(0,9):
        col = {}
        for x in range(0,9):
            col[(x,i)] = new_Grid[x][i]
        cols.append(col)
    return cols
    
def get_all_related_cells(new_Grid):
    squares = get_squares(new_Grid)
    rows = get_rows(new_Grid)
    cols = get_cols(new_Grid)
    all_vec = squares + rows + cols
    return all_vec

def get_legal_for_cell(cell_r, cell_c, new_Grid):
    map = {}
    all_vec = get_all_related_cells(new_Grid)
    for a in all_vec:
        if (cell_r, cell_c) in a.keys():
            del a[(cell_r, cell_c)]
            map.update(a)

    exist = []
    for m in map:
        if not map[m]=='.':
            exist.append(map[m])

    rest = list(set(elements) - set(exist))
    return rest

def get_legal_for_all(new_Grid):
    legal_for_all = {}
    for r in range(0,9):
        for c in range(0,9):
            if new_Grid[r][c]=='.':
                legal_for_all[(r,c)] = get_legal_for_cell(
                                            r, c, new_Grid)
    return legal_for_all

def get_next_cell(new_Grid):
    legal_for_all = get_legal_for_all(new_Grid)
    if len(legal_for_all)>0:
        legal_for_all_list = legal_for_all.values()
        legal_for_all_sorted = sorted(legal_for_all_list,key=len)
        key = legal_for_all.keys()[legal_for_all.values().
                               index(legal_for_all_sorted[0])]
    else:
        key=(10,10)
    return key

def is_complete(new_Grid):
    grid_complete = True
    for r in new_Grid:
        grid_complete = grid_complete and not ('.' in r)
    return grid_complete

def print_grid(new_Grid):
    for item in new_Grid:
        print item
    print

def solve_step_in_sudoko(last_Grid):
    new_Grid = deepcopy(last_Grid)
    complete = False 
    if is_complete(new_Grid):
        complete = True
    r,c = get_next_cell(new_Grid)
    legal_for_cell = get_legal_for_cell(r, c, new_Grid)

    for item in legal_for_cell:
        if complete:
            break
        if not(r==10 and c==10):
            new_Grid[r][c] = item
        returned_Grid = \
                solve_step_in_sudoko(new_Grid)
        if not returned_Grid==None:
            complete = True
            new_Grid = returned_Grid
    if complete:
        return new_Grid

complete_Grid = solve_step_in_sudoko(Grid)
print_grid(complete_Grid)
