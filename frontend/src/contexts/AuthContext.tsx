import {
  createContext,
  useCallback,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import { getMe, login as loginApi, register as registerApi } from "../api/auth";
import type { Player } from "../types/auth";

const TOKEN_KEY = "blockblast_token";

interface AuthContextType {
  token: string | null;
  player: Player | null;
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem(TOKEN_KEY),
  );
  const [player, setPlayer] = useState<Player | null>(null);
  const [error, setError] = useState<string | null>(null);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setPlayer(null);
  }, []);

  // Whenever the token changes, resolve the current player. A rejected /me
  // means the token is stale — drop it so the UI falls back to signed-out.
  useEffect(() => {
    let active = true;
    async function resolvePlayer() {
      if (!token) {
        if (active) setPlayer(null);
        return;
      }
      try {
        const me = await getMe(token);
        if (active) setPlayer(me);
      } catch {
        if (active) logout();
      }
    }
    void resolvePlayer();
    return () => {
      active = false;
    };
  }, [token, logout]);

  const login = useCallback(async (username: string, password: string) => {
    try {
      const { access_token } = await loginApi(username, password);
      localStorage.setItem(TOKEN_KEY, access_token);
      setToken(access_token);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  }, []);

  const register = useCallback(
    async (username: string, password: string) => {
      try {
        await registerApi(username, password);
        await login(username, password);
      } catch (err) {
        setError((err as Error).message);
      }
    },
    [login],
  );

  return (
    <AuthContext.Provider
      value={{ token, player, error, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}
