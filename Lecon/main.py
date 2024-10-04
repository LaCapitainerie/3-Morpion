from json import dump, load
from typing import Optional

from store import session
from store import GameTree

class Node:
    next_grid:int
    current_player:str
    move:tuple[int, int]
    children:list['Node']
    winner:str
    id:int

    def __init__(self, move:tuple[int, int], current_player:str, next_grid:int) -> None:
        self.move = move
        self.current_player = current_player
        self.next_grid = next_grid
        self.children:list['Node'] = []

    def to_dict(self) -> dict:
        """
        Convert the node to a dictionary
        
        :return: The node as a dictionary
        """
        
        return {
            'winner': None,
            'moves': {str(child.move): child.to_dict() for child in self.children}
        }

class Morpion:
    def __init__(self):
        self.board = [['' for _ in range(9)] for _ in range(9)]
        self.super_board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.next_grid:Optional[int] = None

    def print_board(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(self.board[i][j] if self.board[i][j] else '.', end=" ")
            print()
        print()

    def check_winner(self, grid: list[str]) -> str:
        """
        Check if there is a winner in the grid

        :param grid: The grid to check for a winner
        :return: The winner of the grid
        """

        lines = [
            [grid[0], grid[1], grid[2]],
            [grid[3], grid[4], grid[5]],
            [grid[6], grid[7], grid[8]],
            [grid[0], grid[3], grid[6]],
            [grid[1], grid[4], grid[7]],
            [grid[2], grid[5], grid[8]],
            [grid[0], grid[4], grid[8]],
            [grid[2], grid[4], grid[6]],
        ]
        for line in lines:
            if line[0] == line[1] == line[2] and line[0] != '':
                return line[0]
            
        if all(cell != '' for cell in grid):
            return 'Stale'
        
        return ""
    
    def getPossibleMoves(self) -> list[tuple[int, int]]:
        """
        Get all possible moves

        :return: List of possible moves (tuples of (grid, cell))
        """
        
        if isinstance(self.next_grid, int):
            return [(self.next_grid, pos) for pos, j in enumerate(self.board[self.next_grid]) if j == '']
        return [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == '']

    def make_move(self, grid:int, cell:int) -> bool:
        """
        Make a move
        
        :param grid: The grid to make the move in
        :param cell: The cell to make the move in
        :return: True if the move was successful, False otherwise
        """
        
        if self.board[grid][cell] != '' or (self.next_grid is not None and grid != self.next_grid):
            return False

        self.board[grid][cell] = self.current_player

        winner = self.check_winner(self.board[grid])

        if winner:
            self.super_board[grid] = winner

        self.next_grid = cell if self.super_board[cell] == '' else None

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_super_winner(self) -> str:
        """
        Check if there is a winner in the super board
        
        :return: The winner of the super board
        """

        return self.check_winner(self.super_board)

    def generate_move_tree(self, node:Node, depth:int, max_depth:int) -> None:
        """
        Generate the game tree
        
        :param node: The current node in the game tree
        :param depth: The current depth of the game tree
        :param max_depth: The maximum depth to generate the game tree
        """

        if depth >= max_depth:
            return

        winner = self.check_super_winner()
        if winner:
            node.winner = winner
            session.add(node)
            session.commit()
            return

        possible_moves = self.getPossibleMoves()
        for move in possible_moves:
            new_game = Morpion()
            new_game.board = [row[:] for row in self.board]
            new_game.super_board = self.super_board[:]
            new_game.current_player = self.current_player
            new_game.next_grid = self.next_grid

            if new_game.make_move(move[0], move[1]):
                child_node = GameTree(
                    move[0],
                    move[1],
                    new_game.current_player,
                    new_game.next_grid,
                    parent_id=node.id
                )
                session.add(child_node)
                node.children.append(child_node)
                session.commit()
                new_game.generate_move_tree(child_node, depth + 1, max_depth)

    def play(self, max_depth:int=3):
        """
        Play the game
        
        :param max_depth: The maximum depth to generate the game tree
        """
        root = GameTree(None, None, self.current_player, self.next_grid)
        session.add(root)
        session.commit()
        self.generate_move_tree(root, 0, max_depth)

    def save_tree(self, root:Node):
        """
        Save the game tree to a file
        
        :param root: The root node of the game tree
        """
        tree_dict = root.to_dict()
        with open('tree.json', 'w') as f:
            dump(tree_dict, f, indent=4)

    def load_config(self, config_path:str):
        """
        Load the game configuration from a file
        
        :param config_path: The path to the configuration file
        """

        with open(config_path, 'r') as f:
            config = load(f)
        self.board = config['board']
        self.super_board = config['super_board']
        self.current_player = config['current_player']
        self.next_grid = config['next_grid']

if __name__ == "__main__":
    game = Morpion()
    game.play(max_depth=5)


