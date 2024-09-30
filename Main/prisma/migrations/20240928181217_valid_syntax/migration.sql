-- Create the player table
CREATE TABLE "player" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "role" VARCHAR(255) NOT NULL,
    "token" VARCHAR(255) NOT NULL
);

-- Create the game table
CREATE TABLE "game" (
    "id" SERIAL PRIMARY KEY,
    "currentState" VARCHAR(255) NOT NULL
);

-- Create the move table
CREATE TABLE "move" (
    "id" SERIAL PRIMARY KEY,
    "x" INT NOT NULL,
    "y" INT NOT NULL,
    "game_id" INT NOT NULL,
    "player_id" INT NOT NULL,
    FOREIGN KEY ("game_id") REFERENCES "game"("id"),
    FOREIGN KEY ("player_id") REFERENCES "player"("id")
);

-- Create the player_in_game table
CREATE TABLE "player_in_game" (
    "id" SERIAL PRIMARY KEY,
    "player_id" INT NOT NULL,
    "game_id" INT NOT NULL,
    FOREIGN KEY ("player_id") REFERENCES "player"("id"),
    FOREIGN KEY ("game_id") REFERENCES "game"("id")
);