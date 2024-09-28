/*
  Warnings:

  - You are about to drop the `player_in_game` table. If the table is not empty, all the data it contains will be lost.
  - A unique constraint covering the columns `[id]` on the table `game` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[id]` on the table `move` will be added. If there are existing duplicate values, this will fail.

*/
-- DropForeignKey
ALTER TABLE "move" DROP CONSTRAINT "move_game_id_fkey";

-- DropForeignKey
ALTER TABLE "move" DROP CONSTRAINT "move_player_id_fkey";

-- DropForeignKey
ALTER TABLE "player_in_game" DROP CONSTRAINT "player_in_game_game_id_fkey";

-- DropForeignKey
ALTER TABLE "player_in_game" DROP CONSTRAINT "player_in_game_player_id_fkey";

-- AlterTable
ALTER TABLE "game" ALTER COLUMN "currentState" SET DATA TYPE TEXT;

-- AlterTable
ALTER TABLE "player" ALTER COLUMN "name" SET DATA TYPE TEXT,
ALTER COLUMN "email" SET DATA TYPE TEXT,
ALTER COLUMN "password" SET DATA TYPE TEXT,
ALTER COLUMN "role" SET DATA TYPE TEXT,
ALTER COLUMN "token" SET DATA TYPE TEXT;

-- DropTable
DROP TABLE "player_in_game";

-- CreateTable
CREATE TABLE "PlayerInGame" (
    "id" SERIAL NOT NULL,
    "player_id" INTEGER NOT NULL,
    "game_id" INTEGER NOT NULL,

    CONSTRAINT "PlayerInGame_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "game_id_key" ON "game"("id");

-- CreateIndex
CREATE UNIQUE INDEX "move_id_key" ON "move"("id");

-- AddForeignKey
ALTER TABLE "PlayerInGame" ADD CONSTRAINT "PlayerInGame_player_id_fkey" FOREIGN KEY ("player_id") REFERENCES "player"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PlayerInGame" ADD CONSTRAINT "PlayerInGame_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "game"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "move" ADD CONSTRAINT "move_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "game"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "move" ADD CONSTRAINT "move_player_id_fkey" FOREIGN KEY ("player_id") REFERENCES "player"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
