# Initialization
from copy import deepcopy

S = ['1',  '12',  '6', '3',
     '9',  '14',  '2', '5',
     '11', '4',   '15', '*',
     '10', '8',   '13', '7']

G = ['1',  '2',  '3',  '4',
     '5',  '6',  '7',  '8',
     '9',  '10', '11', '12',
     '13', '14', '15', '*']

##mapping S to x,y coordinate plane
coordinates = {0:(0,0),  1:(0,1),  2:(0,2),  3:(0,3),
               4:(1,0),  5:(1,1),  6:(1,2),  7:(1,3),
               8:(2,0),  9:(2,1),  10:(2,2), 11:(2,3),
               12:(3,0), 13:(3,1), 14:(3,2), 15:(3,3)}

##cases = [[move, value, inverse_move], ...]
cases = [['U', -4, 'D'], ['D', 4, 'U'], ['L', -1, 'R'], ['R', 1, 'L']]

no_of_elements = 16
cost = 1

def is_legal_move(move, blank_indx):
    if move == 'U':
        return blank_indx > 3
    elif move == 'D':
        return blank_indx < 12
    elif move == 'L':
        return blank_indx % 4 > 0
    elif move == 'R':
        return blank_indx % 4 < 3

def get_Manhattan_Distance(puzzle, goal):
    mhd = 0
    for i in range(no_of_elements):
        if puzzle[i] == '*' or puzzle[i] == goal[i]:
            continue
        else:
            cell_index_at_goal = goal.index(puzzle[i])
            mhd += abs(coordinates[i][0] - coordinates[cell_index_at_goal][0])
            mhd += abs(coordinates[i][1] - coordinates[cell_index_at_goal][1])
##    mhd = 0         # from 1475 expand to more than 20000 expand
    return mhd

def swap_blank_cell(puzzle, blank_indx, swap_indx):
    new_puzzle = deepcopy(puzzle)
    temp = new_puzzle[blank_indx]
    new_puzzle[blank_indx] = new_puzzle[swap_indx]
    new_puzzle[swap_indx] = temp
    return new_puzzle

def search(puzzle, goal):
    # First Step
    path = []
    g = len(path)
    h = get_Manhattan_Distance(puzzle, goal)
    f = g + h
    open = [[f, g, h, puzzle, path]]
    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find elements to expand

    # Looping    
    while not found and not resign:
        if len(open) == 0:                      # failing
            resign = True
            return 'fail'
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            puzzle = next[3]
            path = next[4]
            g = len(path)

            if puzzle == goal:                  # Goal found
                found = True
                print path
                print 'path length:', len(path)
            else:
                # Add new cells to open list
                blank_indx = puzzle.index('*')
                for i in cases:
                    # check conditions (not reverse move, legal move)
                    move = i[0]
                    rev_move = i[2]
                    if len(path)>0:
                        if rev_move == path[-1]:
                            continue
                    if not is_legal_move(move, blank_indx):
                        continue

                    # swapping, heuristics, append
                    swap_indx = blank_indx + i[1]
                    new_puzzle = swap_blank_cell(puzzle, blank_indx, swap_indx)
                    g2 = g + cost
                    path2 = path + list(i[0])
                    h2 = get_Manhattan_Distance(new_puzzle, goal)
                    f2 = g2 + h2
                    open.append([f2, g2, h2, new_puzzle, path2])
                    
search(S, G)
