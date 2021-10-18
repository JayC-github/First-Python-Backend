# Reusability
# ultimate tic-tac-toe
# grid

from tictactoe import TicTacToe

class UltimateTicTacToe:
    def __init__(self):
        self.grid = [[TicTacToe() for _ in range(3)] for _ in range(3)]
        self.target = None
        self.winning_game = TicTacToe()
        
    def set_target(self, row, col):
        self.target = (row col)
        
        
    def target_game(self):
        return self.grid[self.target[0]][self.target[1]]
    
    def has_empty(self, row, col):
        for r in range(3):
            for c in range(3):
                if self.grid[row][col].value(r,c) is None:
                    return True
        return False

    def place_cross(self, row, col):
        """
        Place 'X' in row, col; where row and col are indices into the
        subgame
        """
        self.target_game().place_corss(row, col)
        if self.winning_game.value(row, col) is None and self.target.winner() == 'X':
            self.winning_game.place_cross(self.target[0], slef.target[1])
        if self.has_empty(row, col):
            self.target = (row, col)
        else:
            self.target = None    
        
    def place_nought(self, row, col):
        """
        Place 'O' in row, col; where row and col are indices into the
        subgame
        """ 
        
        self.target_game().place_corss(row, col)
        if self.winning_game.value(row, col) is None and self.target.winner() == 'O':
            self.winning_game.place_nought(self.target[0], self.target[1])
        if self.has_empty(row, col):
            self.target = (row, col)
        else:
            self.target = None

# can't use different version of librarary
version x.y.z
x = major totally change compatible
y = minor add functionality still compatible 
z = patch make a bug fixed still compatible           

##########################
PyJWT >= 1.7, < 2.0
hypothesis >= 4.44, < 5.0      or >= 4.44, == 4.*



