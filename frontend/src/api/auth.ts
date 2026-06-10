// REST calls for the auth endpoints.
import type { AuthResponse, Player } from "../types/auth";
import { apiFetch } from "./client";

/** POST /api/auth/register — create an account, returns the new player. */
export function register(username: string, password: string): Promise<Player> {
  return apiFetch<Player>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

/** POST /api/auth/token — OAuth2 password flow; returns a bearer token. */
export function login(
  username: string,
  password: string,
): Promise<AuthResponse> {
  return apiFetch<AuthResponse>("/api/auth/token", {
    method: "POST",
    body: new URLSearchParams({ username, password }),
  });
}

/** GET /api/auth/me — resolve the player for a bearer token. */
export function getMe(token: string): Promise<Player> {
  return apiFetch<Player>("/api/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}
