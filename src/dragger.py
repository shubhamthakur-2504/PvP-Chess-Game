import pygame
from const import *


class Dragger:
    def __init__(self) -> None:
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.piece = None
        self.dragging = False

    #blits method/ draging logic

    def update_blits(self,surface):
        #texture
        self.piece.set_Texture(size=128)
        texture = self.piece.texture

        #img
        img = pygame.image.load(texture)

        #rect
        img_center = (self.mouseX , self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        
        #blits
        surface.blit(img, self.piece.texture_rect)


    def update_Mouse(self,pos):
        self.mouseX , self.mouseY = pos # it store the cordinate of (X,Y)


    def save_Initials(self, pos):
       self.initial_row = pos[1] // sqsize
       self.initial_col = pos[0] // sqsize

    def drag_Piece(self,piece):
        self.piece = piece
        self.dragging = True

    def undrag_Piece(self):
        self.piece = None
        self.dragging = False



