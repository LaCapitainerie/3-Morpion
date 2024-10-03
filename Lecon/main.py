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

    def check_winner(self, grid):
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
        return None

    def make_move(self, row, col):
        if self.board[row][col] != '' or (self.next_grid is not None and (row // 3, col // 3) != self.next_grid):
            return False

        self.board[row][col] = self.current_player
        subgrid_index = (row // 3) * 3 + (col // 3)
        subgrid = [self.board[i][j] for i in range(subgrid_index // 3 * 3, subgrid_index // 3 * 3 + 3) for j in range(subgrid_index % 3 * 3, subgrid_index % 3 * 3 + 3)]
        winner = self.check_winner(subgrid)
        if winner:
            self.super_board[subgrid_index] = winner

        self.next_grid = (row % 3, col % 3)
        if self.super_board[self.next_grid[0] * 3 + self.next_grid[1]] != '':
            self.next_grid = None

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_super_winner(self):
        return self.check_winner(self.super_board)

    def play(self):
        while True:
            self.print_board()
            row, col = map(int, input(f"Player {self.current_player}, enter your move (row col): ").split())
            if not self.make_move(row, col):
                print("Invalid move. Try again.")
                continue

            winner = self.check_super_winner()
            if winner:
                self.print_board()
                print(f"Player {winner} wins the game!")
                break

if __name__ == "__main__":
    game = Morpion()
    game.play()