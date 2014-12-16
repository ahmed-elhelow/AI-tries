## Within
class Tree:
    def __init__(self, node):
        self.node = node
        self.childs = []
        self.score = 0
        self.has_score = False
        self.max_node = False
        self.has_min_max = False
        self.is_root = False
    def add_child(self, child):
        self.childs.append(child)
    def give_score(self, score):
        self.score = score
        self.has_score = True

## Within
board = list('123456789')
wins = ((0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6))
evaluation_table = {0 : 0, 1:1, 2:10, 3:1000}

def printboard(brd):
    print
    print('\n-+-+-\n'.join('|'.join(brd[x:x+3]) for x in(0,3,6)))
    print

def score(brd = None):
    if brd is None:
        brd = board[:]
    for w in wins:
        b = brd[w[0]]
        if b in 'XO' and all (brd[i] == b for i in w):
            return b, [i+1 for i in w]
    return None, None

def finished(brd):
    return all (b in 'XO' for b in brd)

def space(brd):
    return [ b for b in brd if b not in 'XO']

def evaluate_leaf(tree, xo='X'):        # computer is 'X'
    brd = tree.node                     # board is in tree.node
    ox = 'O' if xo =='X' else 'X'
    score = 0
    for w in wins:
        count_x=0
        count_o=0
        for i in w:
            if brd[i]==xo:
                count_x += 1
            elif brd[i]==ox:
                count_o += 1
        if count_o==0:
            score += evaluation_table[count_x]
        elif count_x==0:
            score -= evaluation_table[count_o]
    tree.give_score(score)

## Within
def generate_possibilities_min_max(board, xo, tree_branch, level):
    if level==0 or all(score(board)) or finished(tree_branch.node):
        evaluate_leaf(tree_branch)
        return None
    set_min_max(tree_branch, level)
    level-=1
    ox = 'O' if xo =='X' else 'X'
    options  = [int(s)-1 for s in space(board)]
    for choice in options:
        brd = board[:]
        brd[choice] = xo
        tree_node = Tree(brd)
        tree_branch.add_child(tree_node)
        generate_possibilities_min_max(brd, ox, tree_node, level)
    if score_min_max(tree_branch):    # after adding all childs
        return score_min_max(tree_branch)
        
def set_min_max(tree_branch, level):
    if level%2==0:  #even
        tree_branch.max_node = True
        tree_branch.has_min_max = True
    else:
        tree_branch.max_node = False
        tree_branch.has_min_max = True

## Within
def score_min_max(tree_branch):
    if tree_branch.has_min_max:
        if tree_branch.max_node:    # max node
            if tree_branch.is_root:
                max_move = max(tree_branch.childs, key=lambda ch:ch.score)
                return max_move
            else:
                max_score = tree_branch.childs[0].score
                for ch in tree_branch.childs:
                    if ch.score>max_score:
                        max_score = ch.score
                tree_branch.give_score(max_score)
        else:                       # min node
            min_score = tree_branch.childs[0].score
            for ch in tree_branch.childs:
                if ch.score<min_score:
                    min_score = ch.score
            tree_branch.give_score(min_score)

## Within
def min_max_turn(xo):
    global board
    tree = Tree(board)
    tree.is_root = True
    max_move = generate_possibilities_min_max(board, xo, tree, 8)
    choice=list(set(board)-set(max_move.node))
    board = max_move.node
    return choice[0]

def your_turn(xo):
    options = space(board)
    options_str = ''.join(options)
    while True:
        choice = str(
                input("Put your %s in any of these positions: %s\n"
                       %(xo, options_str)) )
        if choice in options_str:
            break
        print( "Whoops I don't understand the input" )
    board[int(choice)-1] = xo
    return choice

def me(xo='X'):
    printboard(board)
    print('I go at', min_max_turn(xo))
##    print('I go at', my_better_turn(xo))
##    print('I go at', my_turn(xo))
    return score()
 
def you(xo='O'):
    printboard(board)
    # Call my_turn(xo) below for it to play itself
    print('You went at', your_turn(xo))
    return score()

def play_XO():
    global board
    board = list('123456789')
    start = input("Enter 1 for you start, Enter 0 for computer start:\n")
    while not finished(board) and not all(score()):
        if start: s = you('O')
        else: s = me('X')
        if s[0]:
            printboard(board)
            print("\n%s wins across %s" % s)
            break
        if not finished(board):
            if start: s = me('X')
            else: s = you('O')
            if s[0]:
                printboard(board)
                print("\n%s wins across %s" % s)
                break
    else:
        print('\nA draw')
play_XO()
