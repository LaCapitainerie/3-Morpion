import { cn } from "@/lib/utils"
import React from "react"

function Morpion({depth, cellId, depthMax}: {depth: number, cellId?: number, depthMax: number}) {
  return (
    <div className="grid grid-cols-3 grid-rows-3 gap-4 h-full w-full justify-around border-gray-500" style={{border: "1px solid black"}}>
        {Array.from({length: 9}, (_, i) => (
            <div key={i} className={cn(depth < depthMax ? "" : ((9*(depthMax - depth) + i + 9*(cellId || 0)) % 2 ? 'bg-lime-800' : 'bg-gray-200'), "hover:bg-opacity-60")}>
              {
                  depth < depthMax ? (
                      <Morpion depth={depth + 1} cellId={i + depth * (cellId || 0)} depthMax={depthMax} />
                  ) : (
                      <span className={`h-full w-full text-accent-foreground`}>
                        {/* {depthMax} {depth} {cellId} {i} */}
                      </span>
                  )
              }
            </div>
        ))}
    </div>
  )
}

export function Morpion3({depth, className}: {depth: number} & React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={className}>
      <Morpion depth={0} depthMax={depth-1} />
    </div>
  )
}
