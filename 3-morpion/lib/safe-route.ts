import { NextResponse } from "next/server";
import { createZodRoute } from 'next-zod-route';
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export class RouteError extends Error {
    status?: number;
    constructor(message: string, status?: number) {
      super(message);
      this.status = status;
    }
  }
  
export const route = createZodRoute({
  handleServerError: (e: Error) => {
    if (e instanceof RouteError) {
      return NextResponse.json(
        { message: e.message, status: e.status },
        {
          status: e.status,
        },
      );
    }

    return NextResponse.json({ message: "Internal server error" }, { status: 500 });
  },
});

export const authRoute = route.use(async ({ request }) => {
  const token = request.headers.get('Authorization');
  if (!token) {
    throw new RouteError('Unauthorized', 401);
  };

  if (!token.startsWith('Bearer ')) {
    throw new RouteError('Unauthorized', 401);
  }

  const tokenValue = token.split('Bearer ')[1];

  const player = await prisma.player.findFirst({
    where: {
      token: tokenValue,
    },
  });

  if (!player) {
    throw new RouteError('Unauthorized', 401);
  };

  return player;
});

export const adminRoute = authRoute.use(async ({ context }) => {

  if (context.role !== 'admin') {
    throw new RouteError('Unauthorized', 401);
  };

  return { context };
});