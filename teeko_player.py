#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import copy
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    # Bonus point for middle position
    mid = [
        [0,0,0,0,0],
        [0,2,2,2,0],
        [0,2,3,2,0],
        [0,2,2,2,0],
        [0,0,0,0,0]
    ]
    count = 0

    def __init__(self):
        """ "AI always go first" - Hobbes
        """
        self.my_piece = self.pieces[0]
        self.opp = self.pieces[1]
        
    """
    This function return a list of successor moves from the given state
    @param state: the state to generate successor from
    @param piece: the color of the current player piece
    @return a list of move (same format as moves return by make_move() function)
    """
    def succ(self, state, piece):
        drop = True
        pos = []
        # Count the number of the pieces of the player who are taking turn
        for row in range(5):
            for col in range(5):
                if state[row][col] == piece:
                    pos.append((row, col))
        
        # If the number of pieces is greater or equal to 4, it is not the drop phase
        if len(pos) >= 4:
            drop = False
            
        succ_list = []
        
        # Generate successor for drop phase if drop is True
        if drop:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        succ_list.append([(row, col)])
        
        # Generate successor for continue playing phase
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
    
    """
    This heuristic function weight the move by adding points for pieces of the
    same color and deduct points for pieces of the different color in its adjacent
    neighborhood
    @param state: the state after the move is mad
    @param move: the move (same format of moves return by make_move() function)
    @param piece: the color of the current player piece
    @return the heuristic value
    """
    def h(self, state, move, piece):
        # Coordinate of the recent move
        y = move[0][0]
        x = move[0][1]
        point = 0
        
        # Add the point for the position
        point = self.mid[y][x]
        
        # Count the number of pieces around, add point for same color, deduct for different
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
            
        # Return negative point for the opponent
        # Divide the point by a large number to keep it between -1 and 1
        if state[y][x] == self.opp:
            return -point/20
        return point/20
    
    """
    This is the max_val function which make decision for the max player using
    alpha beta pruning
    @param state: current state
    @param s: recent move that results in the current state
    @param a: aplha
    @param b: beta
    @param depth: the depth that the function will explore
    """
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
    
    """
    This is the min_val function which make decision for the max player using
    alpha beta pruning
    @param state: current state
    @param s: recent move that results in the current state
    @param a: aplha
    @param b: beta
    @param depth: the depth that the function will explore
    """
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
        
    """
    Return the next move for the AI
    @param state: the state that the AI is going to make a move from
    @return a list of tuple(s) with the first element is the tuple contains the
    coordinate of the destination, if it is not the drop phase, there will be
    another tuple (the second element) contains the coordinate of the starting
    point
    """
    def make_move(self, state):
        if self.count == 0:
            return [(2,2)]
        depth = 5
        if self.count <= 4:
            depth = 3
        move = []
        best = -30
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


# In[2]:


# #
# THE FOLLOWING CODE IS FOR INTERACTIVE GAMEPLAY
#
############################################################################

ai = TeekoPlayer()
piece_count = 0
turn = 0

# drop phase
while piece_count < 8:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            player_move = input("Move (e.g. B3): ")
            while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                player_move = input("Move (e.g. B3): ")
            try:
                ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    piece_count += 1
    turn += 1
    turn %= 2

# move phase - can't have a winner until all 8 pieces are on the board
while ai.game_value(ai.board) == 0:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
        print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            move_from = input("Move from (e.g. B3): ")
            while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                move_from = input("Move from (e.g. B3): ")
            move_to = input("Move to (e.g. B3): ")
            while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                move_to = input("Move to (e.g. B3): ")
            try:
                ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                 (int(move_from[1]), ord(move_from[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    turn += 1
    turn %= 2

ai.print_board()
if ai.game_value(ai.board) == 1:
    print("AI wins! Game over.")
else:
    print("You win! Game over.")

