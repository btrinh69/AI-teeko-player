#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import random
import copy
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    mid = [
        [0,0,0,0,0],
        [0,2,2,2,0],
        [0,2,3,2,0],
        [0,2,2,2,0],
        [0,0,0,0,0]
    ]
    count = 0

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = self.pieces[0]
        self.opp = self.pieces[1]
        self.board = [[' ' for j in range(5)] for i in range(5)]
        self.count = 0
        
    def succ(self, state, piece):
        drop = True
        pos = []
        for row in range(5):
            for col in range(5):
                if state[row][col] == piece:
                    pos.append((row, col))
        
        if len(pos) >= 4:
            drop = False
            
        succ_list = []
        
        if drop:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        succ_list.append([(row, col)])
        
        else:
            for y, x in pos:
                if y-1 >= 0:
                    if state[y-1][x] == ' ':
                        succ_list.append([(y-1, x), (y, x)])
                    if x-1 >= 0 and state[y-1][x-1] == ' ':
                        succ_list.append([(y-1, x-1), (y, x)])
                    if x+1 < 5 and state[y-1][x+1] == ' ':
                        succ_list.append([(y-1, x+1), (y, x)])
                if y+1 < 5:
                    if state[y+1][x] == ' ':
                        succ_list.append([(y+1, x), (y, x)])
                    if x-1 >= 0 and state[y+1][x-1] == ' ':
                        succ_list.append([(y+1, x-1), (y, x)])
                    if x+1 < 5 and state[y+1][x+1] == ' ':
                        succ_list.append([(y+1, x+1), (y, x)])
                if x-1 >= 0 and state[y][x-1] == ' ':
                    succ_list.append([(y, x-1), (y, x)])
                if x+1 < 5 and state[y][x+1] == ' ':
                    succ_list.append([(y, x+1), (y, x)])
                        
        return succ_list
    
    def h(self, state, move, piece):
        y = move[0][0]
        x = move[0][1]
        point = 0
        point = self.mid[y][x]
        if y-1 >= 0:
            if state[y-1][x] == piece:
                point += 2
            elif state[y-1][x] != ' ':
                point -= 1
            if x-1 >= 0:
                if state[y-1][x-1] == piece:
                    point += 2
                elif state[y-1][x-1] != ' ':
                    point -= 1
            if x+1 < 5:
                if state[y-1][x+1] == piece:
                    point += 2
                elif state[y-1][x+1] != ' ':
                    point -= 1
        if y+1 < 5:
            if state[y+1][x] == piece:
                point += 2
            elif state[y+1][x] != ' ':
                point -= 1
            if x-1 >= 0:
                if state[y+1][x-1] == piece:
                    point += 2
                elif state[y+1][x-1] != ' ':
                    point -= 1
            if x+1 <5:
                if state[y+1][x+1] == piece:
                    point += 2
                elif state[y+1][x+1] != ' ':
                    point -= 1
        if x-1 >= 0:
            if state[y][x-1] == piece:
                point += 2
            elif state[y][x-1] != ' ':
                point -= 1
        if x+1 < 5:
            if state[y][x+1] == piece:
                point += 2
            elif state[y][x+1] != ' ':
                point -= 1
            
        if state[y][x] == self.opp:
            return -point/20
        return point/20
    
    def max_val(self, state, s, a, b, depth):
        terminal = self.game_value(state)
        if terminal != 0:
            return terminal
        if depth == 0:
            return self.h(state, s, state[s[0][0]][s[0][1]])
        a = -20
        for move in self.succ(state, self.my_piece):
            succ_ = copy.deepcopy(state)
            if len(move) > 1:
                succ_[move[1][0]][move[1][1]] = ' '
            succ_[move[0][0]][move[0][1]] = self.my_piece
            a = max(a, self.min_val(succ_, move, a, b, depth-1))
            if a >= b:
                return b
        return a
    
    def min_val(self, state, s, a, b, depth):
        terminal = self.game_value(state)
        if terminal != 0:
            return terminal
        if depth == 0:
            return self.h(state, s, state[s[0][0]][s[0][1]])
        b = 20
        for move in self.succ(state, self.opp):
            succ_ = copy.deepcopy(state)
            if len(move) > 1:
                succ_[move[1][0]][move[1][1]] = ' '
            succ_[move[0][0]][move[0][1]] = self.opp
            b = min(b, self.max_val(succ_, move, a, b, depth-1))
            if a >= b:
                return a
        return b
        

    def make_move(self, state):
        if self.count == 0:
            return [(2,2)]
        depth = 4
        if self.count <= 4:
            depth = 3
        move = []
        best = -20
        alpha = -30
        beta = 30
        for s in self.succ(state, self.my_piece):
            succ_ = copy.deepcopy(state)
            if len(s) > 1:
                succ_[s[1][0]][s[1][1]] = ' '
            succ_[s[0][0]][s[0][1]] = self.my_piece
            alpha = self.min_val(succ_, s, alpha, beta, depth)
            if best < alpha:
                best = alpha
                move = s
        # ensure the destination (row,col) tuple is at the beginning of the move list
        return move

    def opponent_move(self, move):
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        
    def place_piece(self, move, piece):
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
        self.count += 1
        
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def game_value(self, state):
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
        # TODO: check / diagonal wins
        for row in [3, 4]:
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row-1][col+1] == state[row-2][col+2] == state[row-3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
                
        # TODO: check 2x2 box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col]==state[row][col+1]==state[row+1][col]==state[row+1][col+1]:
                    return 1 if state[row][col]==self.my_piece else -1
        
        return 0 # no winner yet

class TeekoPlayer2:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    count = 0

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
#         self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0]
        self.my_piece = self.pieces[1]
        self.board = [[' ' for j in range(5)] for i in range(5)]
        self.count = 0

    def succ(self, state, piece):
        drop = True
        pos = []
        for row in range(5):
            for col in range(5):
                if state[row][col] == piece:
                    pos.append((row, col))
        
        if len(pos) >= 4:
            drop = False
            
        succ_list = []
        
        if drop:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        succ_list.append([(row, col)])
        
        else:
            for y, x in pos:
                if y-1 >= 0:
                    if state[y-1][x] == ' ':
                        succ_list.append([(y-1, x), (y, x)])
                    if x-1 >= 0 and state[y-1][x-1] == ' ':
                        succ_list.append([(y-1, x-1), (y, x)])
                    if x+1 < 5 and state[y-1][x+1] == ' ':
                        succ_list.append([(y-1, x+1), (y, x)])
                if y+1 < 5:
                    if state[y+1][x] == ' ':
                        succ_list.append([(y+1, x), (y, x)])
                    if x-1 >= 0 and state[y+1][x-1] == ' ':
                        succ_list.append([(y+1, x-1), (y, x)])
                    if x+1 < 5 and state[y+1][x+1] == ' ':
                        succ_list.append([(y+1, x+1), (y, x)])
                if x-1 >= 0 and state[y][x-1] == ' ':
                    succ_list.append([(y, x-1), (y, x)])
                if x+1 < 5 and state[y][x+1] == ' ':
                    succ_list.append([(y, x+1), (y, x)])
                        
        return succ_list
    
    def make_move(self, state):
        drop_phase = True   # TODO: detect drop phase
        if self.count >= 8:
            drop_phase = False
        if not drop_phase:
            succ_ = self.succ(state, self.my_piece)
            return random.choice(succ_)

        move = []
        (row, col) = (random.randint(0,4), random.randint(0,4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0,4), random.randint(0,4))
            
        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        return move

    def opponent_move(self, move):
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        
    def place_piece(self, move, piece):
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
        self.count += 1
        
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def game_value(self, state):
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
        # TODO: check / diagonal wins
        for row in [3, 4]:
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row-1][col+1] == state[row-2][col+2] == state[row-3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
                
        # TODO: check 2x2 box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col]==state[row][col+1]==state[row+1][col]==state[row+1][col+1]:
                    return 1 if state[row][col]==self.my_piece else -1
        
        return 0 # no winner yet


# In[5]:


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

def sim():
    ai = TeekoPlayer()
    rand = TeekoPlayer2()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
#             ai.print_board()
            start = time.time()
            move = ai.make_move(ai.board)
            if (time.time()-start) >= 5:
                return 0
            ai.place_piece(move, ai.my_piece)
            rand.place_piece(move, rand.opp)
#             print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
    #       move_made = False
#             ai.print_board()
#             print(ai.opp+"'s turn")
            move = rand.make_move(rand.board)
            ai.place_piece(move, ai.opp)
            rand.place_piece(move, rand.my_piece)
#             print("Move: "+str(move[0]))
        
        

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
#             ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            rand.place_piece(move, rand.opp)
#             print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
#             print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
#             ai.print_board()
#             print(ai.opp+"'s turn")
            move = rand.make_move(rand.board)
            ai.place_piece(move, ai.opp)
            rand.place_piece(move, rand.my_piece)
#             print("Move from: "+str(move[1])+" to "+str(move[0]))

        # update the game variables
        turn += 1
        turn %= 2

#     ai.print_board()
    if ai.game_value(ai.board) == 1:
        return 1
    else:
        return -1


# In[7]:


win = 0
lose = 0
overtime = 0
result = {}
for i in range(100):
    val = sim()
    if val in result:
        result[val] += 1
    else:
        result[val] = 1
        
result

