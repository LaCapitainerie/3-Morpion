import { route } from "@/lib/safe-route";
import { PrismaClient } from "@prisma/client";
import { GameSchema } from "@/lib/zodSchema";

const prisma = new PrismaClient();

// export const GET = route
//     .use(async () => {
//     const user = await auth();
  
//     if (!user) {
//       throw new RouteError("Session not found!");
//     }
  
//     return {
//       user,
//     };

export const POST = route
    .body(GameSchema)
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

export const GET = route.query().handler(async () => {
    const games = await prisma.game.findMany();
    return games;
});