import { Adherent } from "@/type/Adherent";
import { useLocalStorage } from "./use-local-storage";

export function useUser() {
    return useLocalStorage<Adherent>("NOMOREWASTEUSER", {} as Adherent);
}