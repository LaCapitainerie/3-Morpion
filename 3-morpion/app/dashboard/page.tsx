import { AppSidebar } from "@/components/app-sidebar"
import { Morpion3 } from "@/components/morpion"
import {
  SidebarLayout,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import { verifyToken } from "@/lib/jwt";

export default async function Page() {
  const { cookies } = await import("next/headers");
  
  const user = verifyToken(cookies().get("player:auth")?.value || "");

  console.log(user);
  

  return (
    <SidebarLayout
      defaultOpen={cookies().get("sidebar:state")?.value === "true"}
    >
      <AppSidebar />
      <main className="flex flex-1 flex-col p-2 transition-all duration-300 ease-in-out">
        <div className="h-full rounded-md border-2 border-dashed p-2">
          <h1>{cookies().get("player:auth")?.value || "pas authentifié"}</h1>
          <SidebarTrigger />
          <Morpion3 depth={2} className="w-[1000px] h-[1000px]"/>
        </div>
      </main>
    </SidebarLayout>
  )
}
