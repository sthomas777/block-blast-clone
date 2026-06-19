import { http, HttpResponse } from "msw";
import { describe, expect, it } from "vitest";

import { server } from "../server";
import { API_BASE, apiFetch } from "../../src/api/client";

describe("apiFetch", () => {
  it("parses a JSON 200 response into the typed body", async () => {
    server.use(
      http.get(`${API_BASE}/items`, () => HttpResponse.json({ ok: true })),
    );

    const body = await apiFetch<{ ok: boolean }>("/items");
    expect(body).toEqual({ ok: true });
  });

  it("sets Content-Type: application/json by default", async () => {
    let receivedContentType: string | null = null;
    server.use(
      http.post(`${API_BASE}/echo`, ({ request }) => {
        receivedContentType = request.headers.get("Content-Type");
        return HttpResponse.json({});
      }),
    );

    await apiFetch("/echo", { method: "POST", body: JSON.stringify({}) });

    expect(receivedContentType).toBe("application/json");
  });

  it("does not set Content-Type for URLSearchParams (lets the browser do it)", async () => {
    // The browser sets `application/x-www-form-urlencoded; boundary=...`
    // automatically for URLSearchParams. We must NOT override that with JSON.
    let receivedContentType: string | null = null;
    server.use(
      http.post(`${API_BASE}/form`, ({ request }) => {
        receivedContentType = request.headers.get("Content-Type");
        return HttpResponse.json({});
      }),
    );

    await apiFetch("/form", {
      method: "POST",
      body: new URLSearchParams({ a: "1" }),
    });

    expect(receivedContentType).toMatch(/application\/x-www-form-urlencoded/);
  });

  it("merges caller-supplied headers (e.g. Authorization)", async () => {
    let receivedAuth: string | null = null;
    server.use(
      http.get(`${API_BASE}/me`, ({ request }) => {
        receivedAuth = request.headers.get("Authorization");
        return HttpResponse.json({});
      }),
    );

    await apiFetch("/me", { headers: { Authorization: "Bearer abc" } });

    expect(receivedAuth).toBe("Bearer abc");
  });

  describe("error handling", () => {
    it("throws an Error with the string `detail` from a 4xx body", async () => {
      server.use(
        http.get(`${API_BASE}/oops`, () =>
          HttpResponse.json(
            { detail: "Username already exists" },
            { status: 409 },
          ),
        ),
      );

      await expect(apiFetch("/oops")).rejects.toThrow(
        "Username already exists",
      );
    });

    it("throws with the first message from a Pydantic validation array", async () => {
      server.use(
        http.get(`${API_BASE}/validate`, () =>
          HttpResponse.json(
            { detail: [{ msg: "field required" }, { msg: "too short" }] },
            { status: 422 },
          ),
        ),
      );

      await expect(apiFetch("/validate")).rejects.toThrow("field required");
    });

    it("falls back to `HTTP <status>` when the body is not JSON", async () => {
      server.use(
        http.get(
          `${API_BASE}/down`,
          () => new HttpResponse("not json", { status: 503 }),
        ),
      );

      await expect(apiFetch("/down")).rejects.toThrow("HTTP 503");
    });

    it("falls back to `HTTP <status>` when the body has no `detail`", async () => {
      server.use(
        http.get(`${API_BASE}/weird`, () =>
          HttpResponse.json({ unrelated: "field" }, { status: 500 }),
        ),
      );

      await expect(apiFetch("/weird")).rejects.toThrow("HTTP 500");
    });
  });
});
