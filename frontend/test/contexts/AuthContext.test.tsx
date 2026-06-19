import {
  act,
  render,
  renderHook,
  screen,
  waitFor,
} from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { describe, expect, it } from "vitest";

import { API_BASE } from "../../src/api/client";
import { useAuth } from "../../src/hooks/useAuth";
import { server } from "../server";
import { AuthProvider } from "../../src/contexts/AuthContext";

const TOKEN_KEY = "blockblast_token";

function wrapper({ children }: { children: React.ReactNode }) {
  return <AuthProvider>{children}</AuthProvider>;
}

describe("AuthProvider", () => {
  describe("initial token state", () => {
    it("starts signed out when localStorage has no token", () => {
      const { result } = renderHook(() => useAuth(), { wrapper });
      expect(result.current.token).toBeNull();
      expect(result.current.player).toBeNull();
    });

    it("loads an existing token from localStorage on mount", async () => {
      window.localStorage.setItem(TOKEN_KEY, "stored-token");

      const { result } = renderHook(() => useAuth(), { wrapper });

      expect(result.current.token).toBe("stored-token");
      // Player resolves asynchronously via /api/auth/me.
      await waitFor(() =>
        expect(result.current.player).toEqual({
          player_id: 1,
          username: "test",
        }),
      );
    });

    it("clears a stale token if /me rejects it", async () => {
      window.localStorage.setItem(TOKEN_KEY, "stale-token");
      server.use(
        http.get(`${API_BASE}/api/auth/me`, () =>
          HttpResponse.json({ detail: "Invalid" }, { status: 401 }),
        ),
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      await waitFor(() => expect(result.current.token).toBeNull());
      expect(result.current.player).toBeNull();
      expect(window.localStorage.getItem(TOKEN_KEY)).toBeNull();
    });
  });

  describe("login", () => {
    it("stores the token, resolves the player, and clears any prior error", async () => {
      const { result } = renderHook(() => useAuth(), { wrapper });

      await act(async () => {
        await result.current.login("test", "supersecret");
      });

      expect(result.current.token).toBe("token-for-test");
      expect(window.localStorage.getItem(TOKEN_KEY)).toBe("token-for-test");
      expect(result.current.error).toBeNull();
      await waitFor(() =>
        expect(result.current.player).toEqual({
          player_id: 1,
          username: "test",
        }),
      );
    });

    it("captures the server error on bad credentials and stays signed out", async () => {
      server.use(
        http.post(`${API_BASE}/api/auth/token`, () =>
          HttpResponse.json(
            { detail: "Invalid Password or Username" },
            { status: 401 },
          ),
        ),
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      await act(async () => {
        await result.current.login("test", "wrong");
      });

      expect(result.current.token).toBeNull();
      expect(result.current.error).toBe("Invalid Password or Username");
    });
  });

  describe("register", () => {
    it("registers and immediately logs in (chains to login)", async () => {
      const { result } = renderHook(() => useAuth(), { wrapper });

      await act(async () => {
        await result.current.register("test", "supersecret");
      });

      expect(result.current.token).toBe("token-for-test");
      await waitFor(() => expect(result.current.player).not.toBeNull());
    });

    it("captures the server error when registration fails", async () => {
      server.use(
        http.post(`${API_BASE}/api/auth/register`, () =>
          HttpResponse.json(
            { detail: "Username already exists" },
            { status: 409 },
          ),
        ),
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      await act(async () => {
        await result.current.register("test", "supersecret");
      });

      expect(result.current.token).toBeNull();
      expect(result.current.error).toBe("Username already exists");
    });
  });

  describe("logout", () => {
    it("clears the token, the player, and localStorage", async () => {
      window.localStorage.setItem(TOKEN_KEY, "stored-token");
      const { result } = renderHook(() => useAuth(), { wrapper });
      await waitFor(() => expect(result.current.player).not.toBeNull());

      act(() => result.current.logout());

      expect(result.current.token).toBeNull();
      expect(result.current.player).toBeNull();
      expect(window.localStorage.getItem(TOKEN_KEY)).toBeNull();
    });
  });

  describe("useAuth outside the provider", () => {
    it("throws a clear error when used without AuthProvider", () => {
      // Suppress the React error boundary log for this expected failure.
      const originalError = console.error;
      console.error = () => undefined;
      try {
        function Probe() {
          useAuth();
          return null;
        }
        expect(() => render(<Probe />)).toThrow(
          /useAuth must be used within AuthProvider/,
        );
      } finally {
        console.error = originalError;
      }
    });

    it("renders the provider's children", () => {
      render(
        <AuthProvider>
          <p>signed-out content</p>
        </AuthProvider>,
      );
      expect(screen.getByText("signed-out content")).toBeInTheDocument();
    });
  });
});
