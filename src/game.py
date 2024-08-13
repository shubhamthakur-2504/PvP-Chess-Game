import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square


class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        self.next_player = 'white'
        self.hovered_sq = None


    #blits methods
    def show_bg(self,surface):
        theme = self.config.theme
        for row in range(Row):
            for col in range(Col):
                #color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                #rect
                rect=(col * sqsize , row * sqsize , sqsize , sqsize)
                #blit
                pygame.draw.rect(surface, color, rect)

                #row cordinates
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    #lable
                    lb = self.config.font.render(str(Row-row),1,color)
                    lb_pos = (5 , 5 + row * sqsize)
                    # blit
                    surface.blit(lb,lb_pos)

                # col cordinate
                if row == 7:
                    color = theme.bg.dark if (row+col) % 2 == 0 else theme.bg.light
                    #lable
                    lb = self.config.font.render(Square.get_alphacol(col) ,1,color)
                    lb_pos = (col*sqsize+sqsize-20,height-20)
                    # blit
                    surface.blit(lb,lb_pos)


    def show_pieces(self,surface):
        for row in range(Row):
            for col in range(Col):
                #pieces?
                if self.board.squares[row][col].has_pieces():
                    piece = self.board.squares[row][col].piece

                    # all pieces except the piece that we are dragging
                    if piece is not self.dragger.piece:
                        piece.set_Texture(80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * sqsize + sqsize // 2 , row * sqsize + sqsize // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img , piece.texture_rect)


    def show_Moves(self,surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece

            #for all valid moves
            for move in piece.moves:
                #color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                #rect
                rect = (move.final.col * sqsize , move.final.row * sqsize , sqsize , sqsize)
                #blit
                pygame.draw.rect(surface,color,rect)

    def show_last_move(self,surface):
        theme = self.config.theme
        if self.board.last_Move:
            initial = self.board.last_Move.initial
            final = self.board.last_Move.final

            for pos in [initial,final]:
                 #color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                #rect
                rect = (pos.col * sqsize , pos.row * sqsize , sqsize , sqsize)
                #blit
                pygame.draw.rect(surface,color,rect)

    def show_hover(self,surface):
        if self.hovered_sq:
             #color
                color = (180,180,180)
                #rect
                rect = (self.hovered_sq.col * sqsize , self.hovered_sq.row * sqsize , sqsize , sqsize)
                #blit
                pygame.draw.rect(surface,color,rect)


    # other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self,row,col):
        self.hovered_sq = self.board.squares[row][col]
    
    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self,captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()