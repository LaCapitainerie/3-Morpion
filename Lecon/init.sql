CREATE TABLE game_tree (
    id SERIAL PRIMARY KEY,
    move_grid INTEGER NOT NULL,
    move_cell INTEGER NOT NULL,
    current_player VARCHAR NOT NULL,
    next_grid INTEGER,
    parent_id INTEGER REFERENCES game_tree(id),
    winner VARCHAR,
    FOREIGN KEY (parent_id) REFERENCES game_tree(id)
);