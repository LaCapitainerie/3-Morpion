import { route } from "@/lib/safe-route";
import { PrismaClient } from "@prisma/client";
import { z } from "zod";


const prisma = new PrismaClient();


/* -- POST -- //
POST /api/users/utils

{
  "name": "string",
  "email": "string",
  "password": "string"
} => {
  "message": "string"
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

    const existingUser = await prisma.player.findFirst({
      where: {
        email: body.email,
      },
    });
      
    if (existingUser) {
      return Response.json({ message: "User already exists" }, { status: 400 });
    };

    try {
      const newUser = await prisma.player.create({
        data: {
          name: body.name,
          email: body.email,
          password: body.password,
          role: "player",
          token: "",
        },
      });

      if (newUser) {
        return Response.json({ message: "User created" }, { status: 200 });
      } else {
        return Response.json({ message: "User not created" }, { status: 500 });
      };
    } catch (err) {
      return Response.json({ message: err.message }, { status: 400 });
    };
  });



/* -- GET -- //
GET /api/users/utils => {
  "id": "string",
  "name": "string",
  "email": "string",
  "password": "string",
  "role": "string",
  "token": "string"
} | {
  "message": "string"
}
// ---------- */
export const GET = route
  .handler(async () => {
  const users = await prisma.player.findMany();
  return Response.json(users, { status: 200 });
  });



/* -- DELETE -- //
DELETE /api/users/utils

{
  "id": "string"
} => {
  "message": "string"
}
// ---------- */
const playerDeleteSchema = z.object({
    id: z.number(),
});
export const DELETE = route
  .body(playerDeleteSchema)
  .handler(async (req, { body }) => {
    
    try{
      const user = await prisma.player.delete({
        where: {
          id: body.id,
        },
      });
  
      if (user) {
        return Response.json({ message: "User deleted" }, { status: 200 });
      } else {
        return Response.json({ message: "User not found" }, { status: 400 });
      };
    } catch (err) {
      return Response.json({ message: err.message }, { status: 400 });
    };
  });
