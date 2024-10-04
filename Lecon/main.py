from itertools import product
import json

class Node:
    next_grid:int
    current_player:str
    move:tuple[int, int]
    children:list['Node']

    def __init__(self, move, current_player, next_grid):
        self.move = move
        self.current_player = current_player
        self.next_grid = next_grid
        self.children = []

    def to_dict(self):
        return {
            'winner': None,
            'moves': {str(child.move): child.to_dict() for child in self.children}
        }

class Morpion:
    def __init__(self):
        self.board = [['' for _ in range(9)] for _ in range(9)]
        self.super_board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.next_grid = None

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
        """
        
        if isinstance(self.next_grid, int):
            return [(self.next_grid, pos) for pos, j in enumerate(self.board[self.next_grid]) if j == '']
        return [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == '']

    def make_move(self, grid:int, cell:int) -> bool:
        
        if self.board[grid][cell] != '' or (self.next_grid is not None and grid != self.next_grid):
            return False

        self.board[grid][cell] = self.current_player

        winner = self.check_winner(self.board[grid])

        if winner:
            self.super_board[grid] = winner

        self.next_grid = cell if self.super_board[cell] == '' else None

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_super_winner(self):
        return self.check_winner(self.super_board)

    def generate_move_tree(self, node, depth, max_depth):
        if depth >= max_depth:
            return

        winner = self.check_super_winner()
        if winner:
            node.winner = winner
            return

        possible_moves = self.getPossibleMoves() #[(i, j) for i in range(9) for j in range(9) if self.board[i][j] == '' and (self.next_grid is None or (i // 3, j // 3) == self.next_grid)]
        # print("possibles_moves", possible_moves)
        for move in possible_moves:
            new_board = [row[:] for row in self.board]
            new_super_board = self.super_board[:]
            new_game = Morpion()
            new_game.board = new_board
            new_game.super_board = new_super_board
            new_game.current_player = self.current_player
            new_game.next_grid = self.next_grid
            if new_game.make_move(move[0], move[1]):
                child_node = Node(move, new_game.current_player, new_game.next_grid)
                node.children.append(child_node)
                new_game.generate_move_tree(child_node, depth + 1, max_depth)

    def play(self, max_depth=3):
        root = Node(None, self.current_player, self.next_grid)
        self.generate_move_tree(root, 0, max_depth)
        self.save_tree(root)

    def save_tree(self, root):
        tree_dict = root.to_dict()
        with open('tree.json', 'w') as f:
            json.dump(tree_dict, f, indent=4)

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        self.board = config['board']
        self.super_board = config['super_board']
        self.current_player = config['current_player']
        self.next_grid = tuple(config['next_grid']) if config['next_grid'] is not None else None

if __name__ == "__main__":
    game = Morpion()
    # Load configuration if needed
    # game.load_config('config.json')
    game.play(max_depth=5)


