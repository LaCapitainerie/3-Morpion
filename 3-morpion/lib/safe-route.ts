import { NextResponse } from "next/server";
import { createZodRoute } from 'next-zod-route';

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