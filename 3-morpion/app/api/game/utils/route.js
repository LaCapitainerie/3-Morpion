import { route } from "@/lib/safe-route";
import { PrismaClient } from "@prisma/client";
import { GameCreateSchema } from "@/lib/zodSchema";

const prisma = new PrismaClient();

export const GET = createZodRoute()
  .params(paramsSchema)
  .query(querySchema)
  .body(bodySchema)
  .handler((request, context) => {
    const { id } = context.params;
    const { search } = context.query;
    const { field } = context.body;

    return Response.json({ id, search, field }), { status: 200 };
  });

export const POST = route
    .body(GameCreateSchema)
    .handler(async (req, { body }) => {
        if (await prisma.game.create({
        data: {
            name: body.name,
            email: body.email,
        },
        })) {
        return { message: "Game created" };
        } else {
        throw new Error("Game not created");
        };
    });