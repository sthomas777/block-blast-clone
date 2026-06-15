// Shared REST plumbing for talking to the FastAPI backend.
// The game itself runs over WebSocket (see hooks/useGameState.ts); this client
// is for the remaining REST endpoints — auth and leaderboard.

export const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

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
 * Typed fetch wrapper: sets JSON headers (unless sending a form body), merges
 * any caller-supplied headers (e.g. Authorization), throws an Error with a
 * useful message on non-2xx responses, and parses the JSON body as T.
 */
export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  // The login endpoint expects an OAuth2 form body, not JSON. When the caller
  // passes URLSearchParams, let the browser set the form Content-Type itself.
  const isForm = options.body instanceof URLSearchParams;

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...(isForm ? {} : { "Content-Type": "application/json" }),
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(await extractErrorMessage(response));
  }

  return response.json() as Promise<T>;
}
