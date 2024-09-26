import { authRoute } from "@/lib/safe-route";
import { z } from "zod";

const querySchema = z.object({
  id: z.string().optional(),
});

export const GET = authRoute
  .query(querySchema)
  .handler((request, context) => {
    
    const user = context.data.user;
    return Response.json({ user }, { status: 200 });
  });

export const POST = authRoute
  .handler((request, context) => {
    const user = context.data.user;
    return Response.json({ user }, { status: 200 });
  });