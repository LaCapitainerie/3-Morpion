import { z } from 'zod';

export const PlayerSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string(),
  password: z.string(),
  role: z.string(),
  moves: z.array(z.object({
    id: z.number(),
    x: z.number(),
    y: z.number(),
    game_id: z.number(),
    player_id: z.number(),
  })),
  games: z.array(z.object({
    id: z.number(),
    player_id: z.number(),
    game_id: z.number(),
  })),
});

export const GameSchema = z.object({
  id: z.number(),
  moves: z.array(z.object({
    id: z.number(),
    x: z.number(),
    y: z.number(),
    game_id: z.number(),
    player_id: z.number(),
  })),
  players: z.array(z.object({
    id: z.number(),
    player_id: z.number(),
    game_id: z.number(),
  })),
  currentState: z.string(),
});

export const GameListSchema = z.array(GameSchema);

export const PlayerListSchema = z.array(PlayerSchema);

export const GameCreateSchema = z.object({
  name: z.string(),
  symbol: z.string(),
});

export const GameJoinSchema = z.object({
  playerId: z.number(),
});

export const GameMoveSchema = z.object({
  playerId: z.number(),
  x: z.number(),
  y: z.number(),
});

export const GameEndSchema = z.object({
  winner: z.string(),
});