import { route } from "@/lib/safe-route";
import { PrismaClient } from "@prisma/client";
import { playerPostSchema, playerDeleteSchema } from "../userSchema";

const prisma = new PrismaClient();


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
        throw new Error("User not created");
      };
    } catch (err) {
      return Response.json({ message: err.message }, { status: 400 });
    }
  });

export const GET = route.handler(async () => {
  const users = await prisma.player.findMany();
  return Response.json(users, { status: 200 });
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