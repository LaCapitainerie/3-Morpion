import { authRoute } from "@/lib/safe-route";
import { z } from "zod";
import { PrismaClient } from "@prisma/client";


const prisma = new PrismaClient();


/* -- GET -- //
GET /api/game/utils
{
  "id": "string"
} => {
  "currentState": "string"
}
// ---------- */
const querySchema = z.object({
  id: z.string().optional(),
});
export const GET = authRoute
  .query(querySchema)
  .handler(async (request, context) => {
    try {
      const { id } = request.query;
      if (id) {
        const game = await prisma.game.findFirst({
          where: {
            id: id,
          },
        });

        if (!game)return Response.json({ error: "game not found" }, { status: 404 });

        return Response.json({ currentState: game.currentState }, { status: 200 });
      };

      return Response.json({ error: "id is required" }, { status: 400 });
    } catch (error) {
      return { error };
    };
  });


/* -- POST -- //
POST /api/game/utils
{} => {
  "id": "string",
  "currentState": "string"
}
// ---------- */
export const POST = authRoute
  .handler(async (request, context) => {
    try {
      const game = await prisma.game.create({
        data: {
          currentState: "         ",
        },
      });

      return Response.json(game, { status: 200 });
    } catch (error) {
      return Response.json({ error }, { status: 500 });
    };
  });