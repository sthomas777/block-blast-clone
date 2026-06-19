import { act, renderHook, waitFor } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { describe, expect, it } from "vitest";

import { API_BASE } from "../../src/api/client";
import { server } from "../server";
import { useMyScores } from "../../src/hooks/useMyScores";

describe("useMyScores", () => {
  it("returns an empty list when no token is provided", () => {
    const { result } = renderHook(() => useMyScores(null));
    expect(result.current.scores).toEqual([]);
  });

  it("fetches scores on mount when a token is provided", async () => {
    const { result } = renderHook(() => useMyScores("token"));

    await waitFor(() => expect(result.current.scores).toHaveLength(2));
    expect(result.current.scores[0].score).toBe(300);
  });

  it("re-fetches when the token changes", async () => {
    const { result, rerender } = renderHook(
      ({ token }: { token: string | null }) => useMyScores(token),
      { initialProps: { token: null as string | null } },
    );
    expect(result.current.scores).toEqual([]);

    rerender({ token: "token" });
    await waitFor(() => expect(result.current.scores).toHaveLength(2));
  });

  it("clears scores when token becomes null", async () => {
    const { result, rerender } = renderHook(
      ({ token }: { token: string | null }) => useMyScores(token),
      { initialProps: { token: "token" as string | null } },
    );
    await waitFor(() => expect(result.current.scores).toHaveLength(2));

    rerender({ token: null });
    await waitFor(() => expect(result.current.scores).toEqual([]));
  });

  it("swallows server errors and resets scores to empty", async () => {
    server.use(
      http.get(`${API_BASE}/api/scores/me`, () =>
        HttpResponse.json({ detail: "boom" }, { status: 500 }),
      ),
    );

    const { result } = renderHook(() => useMyScores("token"));

    // The hook should not throw — it should just stay empty.
    await waitFor(() => expect(result.current.scores).toEqual([]));
  });

  describe("refresh()", () => {
    it("re-fetches the scores on demand", async () => {
      let fetchCount = 0;
      server.use(
        http.get(`${API_BASE}/api/scores/me`, () => {
          fetchCount += 1;
          return HttpResponse.json([
            {
              score_id: fetchCount,
              player_id: 1,
              session_id: null,
              score: fetchCount * 100,
              lines_cleared: 0,
              achieved_at: "2026-01-01T00:00:00Z",
            },
          ]);
        }),
      );

      const { result } = renderHook(() => useMyScores("token"));
      await waitFor(() => expect(result.current.scores[0]?.score).toBe(100));

      act(() => result.current.refresh());

      await waitFor(() => expect(result.current.scores[0]?.score).toBe(200));
    });

    it("is a no-op when there is no token", async () => {
      const { result } = renderHook(() => useMyScores(null));

      act(() => result.current.refresh());
      // No state change, no network call (MSW would error on unhandled requests).
      expect(result.current.scores).toEqual([]);
    });
  });
});
