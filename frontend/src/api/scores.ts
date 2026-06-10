// REST calls for the score endpoints.
import type { Score } from "../types/auth";
import { apiFetch } from "./client";

/** GET /api/scores/me — the authenticated player's scores, highest first. */
export function getMyScores(token: string): Promise<Score[]> {
  return apiFetch<Score[]>("/api/scores/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}
