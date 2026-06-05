// Shared REST plumbing for talking to the FastAPI backend.
// The game itself runs over WebSocket (see hooks/useGameState.ts); this client
// is for the remaining REST endpoints — auth and leaderboard.

export const API_BASE = "http://localhost:8000";

/** Shape of the error bodies our FastAPI backend returns. */
interface ApiErrorBody {
  detail?: string | { msg?: string }[];
}

async function extractErrorMessage(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as ApiErrorBody;
    if (typeof body.detail === "string") {
      return body.detail;
    }
    if (Array.isArray(body.detail) && body.detail[0]?.msg) {
      return body.detail[0].msg;
    }
  } catch {
    // Body wasn't JSON — fall through to the status-code default.
  }
  return `HTTP ${response.status}`;
}

/**
 * Typed fetch wrapper: sets JSON headers, throws an Error with a useful
 * message on non-2xx responses, and parses the JSON body as T.
 */
export async function apiFetch<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    throw new Error(await extractErrorMessage(response));
  }

  return response.json() as Promise<T>;
}
