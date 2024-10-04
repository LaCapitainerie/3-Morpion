from collections import deque
from collections.abc import Sequence
from itertools import product
from typing import Optional, Union

from more_itertools import flatten


class Morpion():
    winner:Optional[str]
    board:deque[Union['Morpion', str]]
    next_grid:Optional[int]

    def __init__(self) -> None:
        """
        Initialize the Morpion class
        """

        self.board = deque(['' for _ in range(9)])
        self.winner = None
        self.next_grid = None

    def check_winner(self) -> Optional[str]:
        """
        Check if there is a winner in the board
        """

        lines = [
            [self.board[0], self.board[1], self.board[2]],
            [self.board[3], self.board[4], self.board[5]],
            [self.board[6], self.board[7], self.board[8]],
            [self.board[0], self.board[3], self.board[6]],
            [self.board[1], self.board[4], self.board[7]],
            [self.board[2], self.board[5], self.board[8]],
            [self.board[0], self.board[4], self.board[8]],
            [self.board[2], self.board[4], self.board[6]],
        ]

        for line in lines:
            if isinstance(line[0], str) and line[0] == line[1] == line[2] and line[0] != '':
                return line[0]
            
        if all(cell != '' for cell in self.board):
            return 'Stale'
        
        return None
    
    def make_move(self, indexes:Sequence[int], player:str) -> bool:
        """
        Make a move in the board
        
        Args:
            indexes (Sequence[int]): Indexes of the move
            player (str): Player to make the move
            
        Returns:
            bool: True if the move was successful, False otherwise
        """


        if isinstance(self.board[indexes[0]], str) and len(indexes) == 1:
            if self.board[indexes[0]] != '':
                raise ValueError('Cell already taken')
            self.board[indexes[0]] = player
            self.winner = self.check_winner()
            return True
        
        if isinstance(self.board[indexes[0]], Morpion):
            tmp = self.board[indexes[0]].make_move(indexes[1:], player) # type: ignore
            if isinstance(tmp, bool) and tmp:
                self.next_grid = indexes[-1]
                return tmp
        
        return False
        
    def getPossibleMoves(self):
        """
        Get all possible moves
        """

        if all(isinstance(cell, str) for cell in self.board):
            return (i for i, cell in enumerate(self.board) if cell == '')

        return [
            product((i,), cell.getPossibleMoves())
            for i, cell in enumerate(self.board)
            if isinstance(cell, Morpion) and (self.next_grid == i or self.next_grid is None)
        ]
    
    def showPossibleMoves(self):
        """
        Print all possible moves
        """

        print('Possible moves:')
        [print(*_) for _ in self.getPossibleMoves()]
        print()


super_morpion = Morpion()
super_morpion.board = deque(Morpion() for _ in range(9))

TREE_MOVE = {}

nextMoves = flatten(super_morpion.getPossibleMoves()) # type: ignore

for move in nextMoves:
    TREE_MOVE[move] = {}
    
print(TREE_MOVE)
