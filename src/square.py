class Square:

    ALPHACOLS = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}


    def __init__(self,row, col, piece=None):
        self.col = col
        self.row = row
        self.piece = piece
        self.alphacols = self.ALPHACOLS[col]

    def __eq__(self,  other) -> bool:
        return self.row == other.row and self.col == other.col

    def has_pieces(self):
        return self.piece != None
    
    def isempty(self):
        return not self.has_pieces()
    
    def has_Teammate(self, color):
        return self.has_pieces() and self.piece.color == color
    
    def has_Rivial(self , color):
        return self.has_pieces() and self.piece.color != color
    
    def isempty_or_Rival(self, color):
        return self.isempty() or self.has_Rivial(color)
    
    @staticmethod
    def in_Range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
        return ALPHACOLS[col]