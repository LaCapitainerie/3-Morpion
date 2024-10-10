CREATE TABLE game_states (
    id SERIAL PRIMARY KEY,
    board_str VARCHAR(81) NOT NULL UNIQUE,  -- 81 chars for the 9x9 board
    next_moves JSON NOT NULL,               -- JSON object to store possible moves
    current_player CHAR(1) NOT NULL,        -- 'X' or 'O'
    next_grid INT                           -- Next grid to play in
);

-- Create an index on the board_str for faster lookups
CREATE INDEX idx_board_str ON game_states (board_str);
