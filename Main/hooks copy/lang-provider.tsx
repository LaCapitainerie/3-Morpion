"use client"

import { lang } from "@/lib/utils";
import { createContext, Dispatch, SetStateAction, useContext } from "react";
import { useLang } from "./use-lang";

const LangContext = createContext<lang>('fr-Fr');
const SetLangContext = createContext<Dispatch<SetStateAction<lang>>>(
    (value) => {
        console.log('Default function:', value);
    }
);

export function useLangContext() {
    return useContext(LangContext);
}

export function useSetLangContext() {
    return useContext(SetLangContext);
}

export function LangContextProvider({ children }: { children: React.ReactNode }) {
    const [theme, setTheme] = useLang();
    return (
        <LangContext.Provider value={theme}>
            <SetLangContext.Provider value={setTheme}>
                {children}
            </SetLangContext.Provider>
        </LangContext.Provider>
    );
}