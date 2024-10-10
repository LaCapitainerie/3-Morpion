from collections import deque
from collections.abc import Generator
from json import dump
from typing import Optional
from numpy import ndarray, zeros

class Node:
    next_grid:Optional[int]
    current_player:str
    upperGrid:Optional[int]
    subGrid:Optional[int]
    children:deque['Node']

    def __init__(self,
        upperGrid:Optional[int],
        subGrid:Optional[int],
        current_player:str,
        next_grid:Optional[int],
    ):
        self.upperGrid = upperGrid
        self.subGrid = subGrid
        self.current_player = current_player
        self.next_grid = next_grid
        self.children = deque()

    def to_dict(self):
        return {
            'turn': self.current_player,
            'winner': None,
            'moves': {f"{child.upperGrid}-{child.subGrid}": child.to_dict() for child in self.children}
        }

    
def check_winner(grid: ndarray, index: int) -> str:
    """
    Check if there is a winner in the grid

    Args:
        grid (ndarray): The grid to check
        index (int): The index of the grid

    Returns:
        str: The winner if there is one, else an empty string
    """

    match index:
        case 0:
            if grid[0] == grid[1] == grid[2] != '':
                return grid[0]
            if grid[0] == grid[3] == grid[6] != '':
                return grid[0]
            if grid[0] == grid[4] == grid[8] != '':
                return grid[0]
        case 1:
            if grid[0] == grid[1] == grid[2] != '':
                return grid[0]
            if grid[1] == grid[4] == grid[7] != '':
                return grid[1]
        case 2:
            if grid[0] == grid[1] == grid[2] != '':
                return grid[0]
            if grid[2] == grid[5] == grid[8] != '':
                return grid[2]
            if grid[2] == grid[4] == grid[6] != '':
                return grid[2]
        case 3:
            if grid[3] == grid[4] == grid[5] != '':
                return grid[3]
            if grid[0] == grid[3] == grid[6] != '':
                return grid[0]
        case 4:
            if grid[3] == grid[4] == grid[5] != '':
                return grid[3]
            if grid[1] == grid[4] == grid[7] != '':
                return grid[1]
            if grid[0] == grid[4] == grid[8] != '':
                return grid[0]
            if grid[2] == grid[4] == grid[6] != '':
                return grid[2]
        case 5:
            if grid[3] == grid[4] == grid[5] != '':
                return grid[3]
            if grid[2] == grid[5] == grid[8] != '':
                return grid[2]
        case 6:
            if grid[6] == grid[7] == grid[8] != '':
                return grid[6]
            if grid[0] == grid[3] == grid[6] != '':
                return grid[0]
            if grid[6] == grid[4] == grid[2] != '':
                return grid[6]
        case 7:
            if grid[6] == grid[7] == grid[8] != '':
                return grid[6]
            if grid[1] == grid[4] == grid[7] != '':
                return grid[1]
        case 8:
            if grid[6] == grid[7] == grid[8] != '':
                return grid[6]
            if grid[2] == grid[5] == grid[8] != '':
                return grid[2]
            if grid[0] == grid[4] == grid[8] != '':
                return grid[0]
            
    if all(cell != '' for cell in grid):
        return 'Stale'
    
    return ""


class Morpion:
    def __init__(self,
            board:ndarray=zeros((9, 9), dtype=str),
            super_board:ndarray=zeros(9, dtype=str),
            current_player:str='X',
            next_grid:Optional[int]=None
        ):
        self.board = board
        self.super_board = super_board
        self.current_player = current_player
        self.next_grid = next_grid
    
    def getPossibleMoves(self) -> Generator[tuple[int, int], None, None]:
        """
        Get all possible moves
        """
        
        if self.next_grid:
            return ((self.next_grid, pos) for pos, j in enumerate(self.board[self.next_grid]) if j == '')
        
        return ((i, j) for i in range(9) for j in range(9) if self.board[i][j] == '')

    def make_move(self, grid:int, cell:int) -> bool:
        """
        Make a move in the game
        
        Args:
            grid (int): The grid where to play
            cell (int): The cell where to play
            
        Returns:
            bool: True if the move is valid, else False
        """
        
        if self.board[grid][cell] != '' or (self.next_grid is not None and grid != self.next_grid):
            return False
        

        self.board[grid][cell] = self.current_player

        
        if (winner := check_winner(self.board[grid], cell)):
            self.super_board[grid] = winner
            check_winner(self.super_board, grid)

        self.next_grid = cell if self.super_board[cell] == '' else None

        self.current_player = 'O' if self.current_player == 'X' else 'X'

        return True

    def generate_move_tree(self, node:Node, depth:int, max_depth:int):
        """
        Generate the move tree
        
        Args:
            node (Node): The node to generate the tree from
            depth (int): The current depth of the tree
            max_depth (int): The maximum depth of the tree
        
        Returns:
            None
        """

        if depth >= max_depth:
            return

        # winner = self.check_super_winner()
        # if winner:
        #     node.winner = winner
        #     return

        for (upperGrid, subGrid) in self.getPossibleMoves():
            
            new_game = Morpion(
                board=self.board.copy(),
                super_board=self.super_board.copy(),
                current_player=self.current_player,
                next_grid=self.next_grid
            )
            
            if new_game.make_move(upperGrid, subGrid):

                child_node = Node(
                    upperGrid=upperGrid,
                    subGrid=subGrid,
                    current_player=new_game.current_player,
                    next_grid=new_game.next_grid
                )

                node.children.append(child_node)
                new_game.generate_move_tree(child_node, depth + 1, max_depth)

    def play(self, max_depth:int=3):
        """
        Play the game
        
        Args:
            max_depth (int): The maximum depth of the tree
        """

        root = Node(None, None, self.current_player, self.next_grid)
        self.generate_move_tree(root, 0, max_depth)
        self.save_tree(root)

    def save_tree(self, root):
        tree_dict = root.to_dict()
        with open('tree.json', 'w') as f:
            dump(tree_dict, f, indent=1)

if __name__ == "__main__":
    game = Morpion()
    game.play(max_depth=4)


