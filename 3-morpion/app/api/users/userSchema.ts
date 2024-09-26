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

export const playerPostSchema = z.object({
    name: z.string(),
    email: z.string(),
    password: z.string(),
});

export const playerDeleteSchema = z.object({
    id: z.number(),
});