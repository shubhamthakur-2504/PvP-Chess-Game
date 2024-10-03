from const import *
from square import Square
from piece import *
from move import Move
import copy

class Board:
    def __init__(self) -> None:
        self.squares = [[0,0,0,0,0,0,0,0,] for col in range(Col)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_Move = None

    def move(self, piece, move):
        initial =  move.initial
        final = move.final

        #console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        #pawn promotion
        if isinstance(piece , Pawn):
            self.check_promotion(piece, final)

        #king castling
        if isinstance(piece,King):
            if self.castling(initial,final):
                diff=final.col-initial.col
                rook=piece.left_rook if (diff<0) else piece.right_rook
                self.move(rook,rook.moves[-1])

        piece.moved = True

        #clear valid moves
        piece.clear_Moves()

        #set last move
        self.last_Move = move

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7 :
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    def castling(self,initial,final):
        return abs(initial.col-final.col)==2
    
    def in_checks(self,piece,move):
        temp_piece=copy.deepcopy(piece)
        temp_board=copy.deepcopy(self)
        temp_board.move(temp_piece,move)

        for row in range(Row):
            for col in range(Col):
                if temp_board.squares[row][col].has_Rivial(piece.color):
                    p=temp_board.squares[row][col].piece
                    temp_board.calc_Moves(p,row,col , bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece,King):
                            return True
        return False


    def calc_Moves(self, piece,row , col , bool=True):
        '''
            calculate all the possible (valid)  moves of a specific pieces on a specific position
        '''

        def pawn_Moves():
            #steps
            steps = 1 if piece.moved else 2

            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_Move_row in range (start, end, piece.dir):
                if Square.in_Range(possible_Move_row):
                    if self.squares[possible_Move_row][col].isempty(): #to check square to move is empty or not
                        # create initial and final move squares
                        initial = Square(row,col)
                        final =Square(possible_Move_row,col)

                        #create a new move
                        move = Move(initial , final)
                        if bool:
                            if not self.in_checks(piece,move):
                                #append new move
                                piece.add_Move(move)
                        else:
                             #append new move
                            piece.add_Move(move)
                    # if pawn is blocked
                    else: break
                # not in range
                else:break

            #diagonal moves
            possible_Move_row = row + piece.dir
            possible_Move_cols = [col-1, col+1]
            for possible_Move_col in possible_Move_cols:
                if Square.in_Range(possible_Move_row, possible_Move_col):
                    if self.squares[possible_Move_row][possible_Move_col].has_Rivial(piece.color):
                        # create initial and final move squares
                        initial = Square(row,col)
                        final_piece=self.squares[possible_Move_row][possible_Move_col].piece
                        final =Square(possible_Move_row,possible_Move_col,final_piece)

                        #create a new move
                        move = Move(initial , final)
                        if bool:
                            if not self.in_checks(piece,move):
                                #append new move
                                piece.add_Move(move)
                        else:
                             #append new move
                            piece.add_Move(move)

        def kinght_Moves():
            #possible moves for knight
            possible_Moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1)

            ]
            for possible_move in possible_Moves:
                possible_move_row , possible_move_col = possible_move

                if Square.in_Range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_Rival(piece.color):
                        #create square of the new move
                        initial = Square(row,col)
                        final_piece=self.squares[possible_move_row][possible_move_col].piece
                        final =Square(possible_move_row,possible_move_col,final_piece)
                        #create move
                        move = Move(initial , final)
                        if bool:
                            if not self.in_checks(piece,move):
                                #append new move
                                piece.add_Move(move)
                            else:break
                        else:
                             #append new move
                            piece.add_Move(move)

        def strightline_Moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True :
                    if Square.in_Range(possible_move_row,possible_move_col):

                        #create square of the new move
                        initial = Square(row,col)
                        final_piece=self.squares[possible_move_row][possible_move_col].piece
                        final =Square(possible_move_row,possible_move_col,final_piece)
                        #create move
                        move = Move(initial , final)

                        # if empty 
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            if bool:
                                if not self.in_checks(piece,move):
                                    #append new move
                                    piece.add_Move(move)
                            else:
                                #append new move
                                piece.add_Move(move)

                        # has enemy 
                        elif self.squares[possible_move_row][possible_move_col].has_Rivial(piece.color):
                            if bool:
                                if not self.in_checks(piece,move):
                                    #append new move
                                    piece.add_Move(move)
                            else:
                                #append new move
                                piece.add_Move(move)
                            break

                        # has team piece
                        elif self.squares[possible_move_row][possible_move_col].has_Teammate(piece.color):
                            break

                    #outside range
                    else:break

                    # incrementing incrs
                    possible_move_row , possible_move_col = possible_move_row + row_incr , possible_move_col + col_incr

        def king_Walk():
            #possible king moves
            possible_moves = [
                (row-1,col+0),#up
                (row-1,col+1),#up-right
                (row+0,col+1),#right
                (row+1,col+1),#down-right
                (row+1,col+0),#down
                (row+1,col-1),#down-left
                (row+0,col-1),#left
                (row-1,col-1)#up-left
            ]

            #normal moves
            for possible_move in possible_moves:
                possible_move_row , possible_move_col = possible_move

                if Square.in_Range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_Rival(piece.color):
                        #create square of the new move
                        initial = Square(row,col)
                        #piece=piece
                        final =Square(possible_move_row,possible_move_col)
                        #create move
                        move = Move(initial , final)
                        if bool:
                            if not self.in_checks(piece,move):
                                #append new move
                                piece.add_Move(move)
                            else:break
                        else:
                             #append new move
                            piece.add_Move(move)
            
            #castling moves
            if not piece.moved:

                #queenside castle
                left_rook=self.squares[row][0].piece
                if isinstance(left_rook,Rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            #castling is not possible as there are pieces in between
                            if self.squares[row][c].has_pieces():
                                break
                            if c==3 :
                                #add left rook to king
                                piece.left_rook=left_rook

                                #rook moves
                                initial=Square(row,0)
                                final=Square(row,3) 
                                moveR=Move(initial,final)
                                
                                #king move
                                initial=Square(row,col)
                                final=Square(row,2) 
                                moveK=Move(initial,final)
                                if bool:
                                    if not self.in_checks(piece,moveK) and not self.in_checks(left_rook,moveR):
                                        #append new move
                                        left_rook.add_Move(moveR)
                                        piece.add_Move(moveK)
                                    else:break
                                else:
                                    #append new move
                                    left_rook.add_Move(moveR)
                                    piece.add_Move(moveK)

                #kingside castle
                right_rook=self.squares[row][7].piece
                if isinstance(right_rook,Rook):
                    if not right_rook.moved:
                        for c in range(5,7):
                            #castling is not possible as there are pieces in between
                            if self.squares[row][c].has_pieces():
                                break
                            if c==6 :
                                #add left rook to king
                                piece.right_rook=right_rook

                                #rook moves
                                initial=Square(row,7)
                                final=Square(row,5) 
                                moveR=Move(initial,final)
                                
                                #king move
                                initial=Square(row,col)
                                final=Square(row,6) 
                                moveK=Move(initial,final)
                                if bool:
                                    if not self.in_checks(piece,moveK) and not self.in_checks(right_rook,moveR):
                                        #append new move
                                        right_rook.add_Move(moveR)
                                        piece.add_Move(moveK)
                                    else:break
                                else:
                                    #append new move
                                    right_rook.add_Move(moveR)
                                    piece.add_Move(moveK)



        if isinstance(piece, Pawn):
            pawn_Moves()
        elif isinstance(piece , Knight):
            kinght_Moves()
        elif isinstance(piece , Bishop):
            strightline_Moves([
                (-1,1), #up-right
                (-1,-1), #up-left
                (1,1), #down-right
                (1,-1) #down-left
            ])
        elif isinstance(piece , Rook):
            strightline_Moves([
                (-1,0), #up
                (1,0),#down
                (0,1), #right
                (0,-1)#left
            ])
        elif isinstance(piece , Queen):
            strightline_Moves([
                (-1,1), #up-right
                (-1,-1), #up-left
                (1,1), #down-right
                (1,-1), #down-left
                (-1,0), #up
                (1,0),#down
                (0,1), #right
                (0,-1)#left
            ])
        elif isinstance(piece , King):
            king_Walk()

    # create squares
    def _create(self):
        for row in range(Row):
            for col in range(Col):
                self.squares[row][col] = Square(row,col)
            

    def _add_pieces(self,color):
        row_pawn, row_other = (6,7) if color == 'white' else (1,0)

        #pawn
        for col in range (Col):
            self.squares[row_pawn][col] = Square(row_pawn,col,Pawn(color))

        #Knight
        self.squares[row_other][1] = Square(row_other,1,Knight(color))
        self.squares[row_other][6] = Square(row_other,6,Knight(color))

        #Bishop
        self.squares[row_other][2] = Square(row_other,2,Bishop(color))
        self.squares[row_other][5] = Square(row_other,5,Bishop(color))

        #Rook
        self.squares[row_other][0] = Square(row_other,0,Rook(color))
        self.squares[row_other][7] = Square(row_other,7,Rook(color))

        #Queen
        self.squares[row_other][3] = Square(row_other,3,Queen(color))

        #King
        self.squares[row_other][4] = Square(row_other,4,King(color))