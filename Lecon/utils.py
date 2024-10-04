from store import session
from store import GameTree

def calculate_win_percentage(board_state, player):
    # Query all nodes that match the current board state
    possible_moves = session.query(GameTree).filter_by(board_state=board_state).all()

    total_moves = len(possible_moves)
    if total_moves == 0:
        return 0.0

    winning_moves = [move for move in possible_moves if move.winner == player]

    win_percentage = len(winning_moves) / total_moves * 100
    return win_percentage

def find_best_move(board_state, player):
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