import { http, HttpResponse } from "msw";

const API_BASE = "http://localhost:8000";

export const handlers = [
  http.post(`${API_BASE}/api/auth/register`, async ({ request }) => {
    const body = (await request.json()) as { username: string };
    return HttpResponse.json({ player_id: 1, username: body.username });
  }),

  http.post(`${API_BASE}/api/auth/token`, async ({ request }) => {
    const form = await request.formData();
    return HttpResponse.json({
      access_token: `token-for-${form.get("username")}`,
      token_type: "bearer",
    });
  }),

  http.get(`${API_BASE}/api/auth/me`, ({ request }) => {
    const auth = request.headers.get("Authorization");
    if (!auth?.startsWith("Bearer ")) {
      return HttpResponse.json(
        { detail: "Not authenticated" },
        { status: 401 },
      );
    }
    return HttpResponse.json({ player_id: 1, username: "test" });
  }),

  http.get(`${API_BASE}/api/scores/me`, ({ request }) => {
    const auth = request.headers.get("Authorization");
    if (!auth?.startsWith("Bearer ")) {
      return HttpResponse.json(
        { detail: "Not authenticated" },
        { status: 401 },
      );
    }
    return HttpResponse.json([
      {
        score_id: 1,
        player_id: 1,
        session_id: null,
        score: 300,
        lines_cleared: 30,
        achieved_at: "2026-01-01T00:00:00Z",
      },
      {
        score_id: 2,
        player_id: 1,
        session_id: null,
        score: 100,
        lines_cleared: 10,
        achieved_at: "2026-01-02T00:00:00Z",
      },
    ]);
  }),
];
