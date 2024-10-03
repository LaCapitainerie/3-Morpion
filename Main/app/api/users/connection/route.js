import { route } from "@/lib/safe-route";
import { PrismaClient } from "@prisma/client";
import { generateToken } from "@/lib/jwt";
import { z } from "zod";


const prisma = new PrismaClient();


/* -- POST -- //
POST /api/users/connection

{
  "email": "string",
  "password": "string"
} => {
  "token": "string"
}
// ---------- */
const playerPostSchema = z.object({
  name: z.string(),
  email: z.string(),
  password: z.string(),
});
export const POST = route
  .body(playerPostSchema)
  .handler(async (req, { body }) => {

    try {
      const user = await prisma.player.findFirst({
        where: {
          email: body.email,
        },
      });

      if(!user) {
        try {
          await fetch("/api/users/utils", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
          });
        } catch (error) {
          return Response.json({ message: error }, { status: 200 });
        };
      };

      const newUser = user || await prisma.player.findFirst({
        where: {
          email: body.email,
        },
      });

      if(!newUser) {
        return Response.json({ message: "User not created" }, { status: 500 });
      };

      console.log(generateToken({...newUser, password: '',  token: ''}, '1h'));
        
      const jwt = await prisma.player.update({
        where: {
          id: newUser.id,
        },
        data: {
          token: generateToken({...newUser, password: '',  token: ''}, '1h'),
        },
      });

      return Response.json({ token: jwt.token }, { status: 200 });
    } catch (err) {
      return Response.json({ message: err.message }, { status: 400 });
    };
  });