from store import session
from store import GameTree

def calculate_win_percentage(board_state, player:str) -> float:
    """
    Calculate the win percentage for a given player on a given board state
    
    :param board_state: The board state to calculate the win percentage for
    :param player: The player to calculate the win percentage for
    :return: The win percentage for the given player on the given board state
    """

    possible_moves = session.query(GameTree).filter_by(board_state=board_state).all()

    total_moves = len(possible_moves)
    if total_moves == 0:
        return 0.0

    winning_moves = [move for move in possible_moves if str(move.winner) == player]

    win_percentage = len(winning_moves) / total_moves * 100
    return win_percentage

def find_best_move(board_state, player:str) -> GameTree:
    """
    Find the best move for a given player on a given board state

    :param board_state: The board state to find the best move for
    :param player: The player to find the best move for
    :return: The best move for the given player on the given board state
    """

    # Query all possible moves for the current board state
    possible_moves = session.query(GameTree).filter_by(board_state=board_state).all()

    best_move = None
    best_win_percentage = -1

    for move in possible_moves:
        win_percentage = calculate_win_percentage(move.board_state, player)
        if win_percentage > best_win_percentage:
            best_win_percentage = win_percentage
            best_move = move

    return best_move



def get_possible_moves(game_id: int) -> list[tuple[int, int]]:
    """
    Get all possible moves from the current board state of a specific game.
    :param game_id: The ID of the game in the database.
    :return: List of possible moves (tuples of (grid, cell)).
    """

    # Get the game state from the database
    game_state = session.query(GameTree).filter_by(id=game_id).first()

    if not game_state:
        raise ValueError(f"No game state found for game_id: {game_id}")

    board = game_state.board  # 9x9 board (list of lists)
    super_board = game_state.super_board  # Super board state (list)
    next_grid = game_state.next_grid  # The grid where the next move must happen
    possible_moves = []

    # If a specific grid is required to play in (`next_grid` is not None)
    if next_grid is not None:
        if super_board[next_grid] == '':  # Only if the grid isn't already won/tied
            # Look for empty cells in that grid
            for cell, value in enumerate(board[next_grid]):
                if value == '':  # Empty cell means a valid move
                    possible_moves.append((next_grid, cell))
    
    # If any grid can be played in (when `next_grid` is None)
    else:
        for grid in range(9):
            if super_board[grid] == '':  # Only look in grids that aren't won/tied
                for cell, value in enumerate(board[grid]):
                    if value == '':  # Empty cell means a valid move
                        possible_moves.append((grid, cell))

    return possible_moves
