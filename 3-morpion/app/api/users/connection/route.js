import { route } from "@/lib/safe-route";
import { PrismaClient } from "@prisma/client";
import { playerPostSchema } from "../userSchema";
import { generateToken } from "@/lib/jwt";


// -- Connection route -- //
// POST /api/users/connection
// GET /api/users/connection
// -- Connection route -- //


const prisma = new PrismaClient();

export const POST = route
  .body(playerPostSchema)
  .handler(async (req, { body }) => {

    try {

      const user = await prisma.player.findFirst({
        where: {
          email: body.email,
        },
      });

      if (user) {
        
        const jwt = await prisma.player.update({
          where: {
            id: user.id,
          },
          data: {
            token: generateToken({...user, password: '',  token: ''}, '1h'),
          },
        });

        return Response.json({ jwt: jwt }, { status: 200 });
      } else {
        throw new Error("User not connected");
      };



    } catch (err) {
      return Response.json({ message: err }, { status: 400 });
    }
  });

export const GET = route.handler(async () => {
  const users = await prisma.player.findMany();
  return Response.json(users, { status: 200 });
});