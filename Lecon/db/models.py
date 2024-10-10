from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GameState(Base):
    __tablename__ = 'game_states'

    id = Column(Integer, primary_key=True)
    board_str = Column(String, nullable=False, unique=True)  # Unique string for board state
    next_moves = Column(JSON)  # JSON object to store possible next moves
    current_player = Column(String(1), nullable=False)  # 'X' or 'O'
    next_grid = Column(Integer, nullable=True)  # The grid to play in next
