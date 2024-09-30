"use client"

import * as React from "react"

export type Player = {
    id: string
    name: string
    email: string
    password: string
    role: string
    token: string
}

export type AuthContext = {
    player: Player | undefined;
    onPlayerDataChange: (playerValue: Player) => void;
}

export const PLAYER_AUTH_COOKIE = "player:auth"

export function useAuth() {
    const [player, setPlayer] = React.useState<Player>()

    const onPlayerDataChange = React.useCallback((playerValue: Player) => {
        setPlayer(playerValue)
        document.cookie = `${PLAYER_AUTH_COOKIE}=${JSON.stringify(playerValue)}; path=/; max-age=${
          60 * 60 * 24 * 7
        }`
    }, [])

    return {
        player: player,
        onPlayerDataChange: onPlayerDataChange,
    }
}
