from collections import deque
from collections.abc import Sequence
from itertools import product
from typing import Optional, Union


class Morpion():
    winner:Optional[str]
    board:deque[Union['Morpion', str]]
    next_grid:Optional[int]

    def __init__(self):
        self.board = deque('' for _ in range(9))
        self.winner = None
        self.next_grid = None

    def check_winner(self):
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
    
    def make_move(self, indexes:Sequence[int], player:str):

        if len(indexes) == 1:
            if self.board[indexes[0]] != '':
                raise ValueError('Cell already taken')
            self.board[indexes[0]] = player
            self.winner = self.check_winner()
            return True
        
        tmp = self.board[indexes[0]].make_move(indexes[1:], player) # type: ignore
        if tmp:
            self.next_grid = indexes[-1]
            return tmp
        
    def getPossibleMoves(self):

        if all(isinstance(cell, str) for cell in self.board):
            return (i for i, cell in enumerate(self.board) if cell == '')

        return [
            product((i,), cell.getPossibleMoves())
            for i, cell in enumerate(self.board)
            if isinstance(cell, Morpion) and self.next_grid == i
        ]
    
    def showPossibleMoves(self):
        [print(*_) for _ in self.getPossibleMoves()]


_3morpion = Morpion()
_3morpion.board = deque(Morpion() for _ in range(9))

_3morpion.make_move([0, 7], 'X')
_3morpion.showPossibleMoves()
_3morpion.make_move([7, 3], 'O')
_3morpion.showPossibleMoves()
_3morpion.make_move([3, 7], 'X')
_3morpion.showPossibleMoves()


