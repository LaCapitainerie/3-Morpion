from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Setup SQLAlchemy Base and Engine
Base = declarative_base()

# Create the engine for PostgreSQL
engine = create_engine('postgresql://user:password@localhost:5433/tree', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class GameTree(Base):
    __tablename__ = 'game_tree'

    id = Column(Integer, primary_key=True, autoincrement=True)
    move_grid = Column(Integer)
    move_cell = Column(Integer)
    current_player = Column(String)
    next_grid = Column(Integer, nullable=True)
    parent_id = Column(Integer, ForeignKey('game_tree.id'), nullable=True)
    winner = Column(String, nullable=True)
    children = relationship("GameTree", backref="parent", remote_side=[id])

    def __init__(self, move_grid, move_cell, current_player, next_grid, winner=None, parent_id=None):
        self.move_grid = move_grid
        self.move_cell = move_cell
        self.current_player = current_player
        self.next_grid = next_grid
        self.winner = winner
        self.parent_id = parent_id