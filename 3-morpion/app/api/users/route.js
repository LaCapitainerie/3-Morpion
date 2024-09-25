import { route } from "@/lib/safe-route";
import { PrismaClient } from "@prisma/client";
import { PlayerSchema } from "@/lib/zodSchema";

const prisma = new PrismaClient();

export const POST = route
  .body(PlayerSchema)
  .handler(async (req, { body }) => {
    if (await prisma.player.create({
      data: {
        name: body.name,
        email: body.email,
      },
    })) {
      return { message: "User created" };
    } else {
      throw new Error("User not created");
    };
  });

export const GET = route.handler(async () => {
  const users = await prisma.player.findMany();
  return users;
});