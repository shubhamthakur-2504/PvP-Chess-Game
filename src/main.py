#python inbuilt class or modules
import pygame
import sys


#user build class
from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init() #initialize pygame
        self.screen = pygame.display.set_mode((width , height)) #set size of screen using const file
        pygame.display.set_caption("CHESS") 
        self.game=Game() #refrence to game class

    def MainLoop(self):
        game = self.game # so i dont have to write self everytime calling this functions
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
  
        while True:

            #show methods
            game.show_bg(screen) # calling bg function from Game class #screen is prameter recived by showbg function as surface
            game.show_last_move(screen) #shows last move
            game.show_Moves(screen)#shows the possible moves of clicked piece
            game.show_hover(screen)
            game.show_pieces(screen)# calling piece function from game class to show pieces on screen

            if dragger.dragging:
                dragger.update_blits(screen)
            for event in pygame.event.get():

                #click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_Mouse(event.pos)

                    # to get the row and col of clicked square
                    clicked_row = dragger.mouseY // sqsize
                    clicked_col = dragger.mouseX // sqsize

                    #test logic how we get row and col
                    # print(clicked_row , dragger.mouseY)
                    # print(clicked_col, dragger.mouseX)
                    # print(sqsize) #its size is 100


                    # to check if clicked square has a piece or not
                    if board.squares[clicked_row][clicked_col].has_pieces():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color)?
                        if piece.color == game.next_player:

                            board.calc_Moves(piece,clicked_row,clicked_col,bool=True)
                            dragger.save_Initials(event.pos) # saves the initial position of piece
                            dragger.drag_Piece(piece)
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen) 
                            game.show_Moves(screen)
                            game.show_pieces(screen)


                
                #moving event/ Mouse motion
                elif event.type == pygame.MOUSEMOTION:

                    motion_row = event.pos[1] // sqsize
                    motion_col = event.pos[0] // sqsize

                    game.set_hover(motion_row,motion_col)

                    if dragger.dragging:
                        dragger.update_Mouse(event.pos)
                        #show moves
                        game.show_bg(screen)
                        game.show_last_move(screen) 
                        game.show_Moves(screen)
                        game.show_hover(screen)
                        game.show_pieces(screen)
                        dragger.update_blits(screen)

                #click release event
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_Mouse(event.pos)

                        release_row = dragger.mouseY // sqsize
                        release_col = dragger.mouseX // sqsize

                        # creating possible move
                        initial = Square(dragger.initial_row,dragger.initial_col)
                        final = Square(release_row, release_col)
                        move = Move(initial, final)

                        # valid move?
                        if board.valid_move(dragger.piece,move):
                            captured = board.squares[release_row][release_col].has_pieces()
                            board.move(dragger.piece, move) 

                            board.set_en_passant_True(dragger.piece)

                            #sound
                            game.sound_effect(captured)

                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            #next turn
                            game.next_turn()


                    dragger.undrag_Piece()

                #key events
                elif event.type == pygame.KEYDOWN:
                    
                    #changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    #restart game
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game 
                        dragger = self.game.dragger
                        board = self.game.board

                #game quit event
                elif event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main=Main()
main.MainLoop()