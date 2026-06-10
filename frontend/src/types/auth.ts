// Auth + score contracts (mirror the backend schemas/auth.py & schemas/score.py).

/** Returned by POST /api/auth/token. */
export interface AuthResponse {
  access_token: string;
  token_type: string;
}

/** Returned by /api/auth/register and /api/auth/me. */
export interface Player {
  player_id: number;
  username: string;
}

/** A single saved score, returned by GET /api/scores/me. */
export interface Score {
  score_id: number;
  player_id: number;
  session_id: number | null;
  score: number;
  lines_cleared: number;
  achieved_at: string;
}
