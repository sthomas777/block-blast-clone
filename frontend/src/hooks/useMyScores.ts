import { useCallback, useEffect, useState } from "react";

import { getMyScores } from "../api/scores";
import type { Score } from "../types/auth";

/**
 * The signed-in player's scores. Returns a `refresh` callback so callers can
 * re-fetch after a game ends. Without a token it stays empty.
 *
 * All state updates happen in async callbacks (never synchronously inside the
 * effect) to avoid cascading renders.
 */
export function useMyScores(token: string | null) {
  const [scores, setScores] = useState<Score[]>([]);

  const refresh = useCallback(() => {
    if (!token) return;
    getMyScores(token)
      .then(setScores)
      .catch(() => setScores([]));
  }, [token]);

  // Load (or clear) scores whenever the signed-in identity changes.
  useEffect(() => {
    let active = true;
    async function load() {
      if (!token) {
        if (active) setScores([]);
        return;
      }
      try {
        const data = await getMyScores(token);
        if (active) setScores(data);
      } catch {
        if (active) setScores([]);
      }
    }
    void load();
    return () => {
      active = false;
    };
  }, [token]);

  return { scores, refresh };
}
