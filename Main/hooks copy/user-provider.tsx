"use client"

import { createContext, Dispatch, SetStateAction, useContext } from "react";
import { useUser } from "./use-user";
import { Adherent } from "@/type/Adherent";

const UserContext = createContext<Adherent>({} as Adherent);
const SetUserContext = createContext<Dispatch<SetStateAction<Adherent>>>(
    (value) => {
        console.log('Default function:', value);
    }
);

export function useUserContext() {
    return useContext(UserContext);
}

export function useSetUserContext() {
    return useContext(SetUserContext);
}

export function UserContextProvider({ children }: { children: React.ReactNode }) {
    const [theme, setTheme] = useUser();
    return (
        <UserContext.Provider value={theme}>
            <SetUserContext.Provider value={setTheme}>
                {children}
            </SetUserContext.Provider>
        </UserContext.Provider>
    );
}