import "@testing-library/jest-dom/vitest";

import { cleanup } from "@testing-library/react";
import { afterAll, afterEach, beforeAll } from "vitest";

import { server } from "./server";

function createMemoryStorage(): Storage {
  const map = new Map<string, string>();
  return {
    get length() {
      return map.size;
    },
    clear() {
      map.clear();
    },
    getItem(key) {
      return map.get(key) ?? null;
    },
    setItem(key, value) {
      map.set(key, String(value));
    },
    removeItem(key) {
      map.delete(key);
    },
    key(index) {
      return [...map.keys()][index] ?? null;
    },
  };
}

const memoryStorage = createMemoryStorage();

Object.defineProperty(globalThis, "localStorage", {
  value: memoryStorage,
  configurable: true,
});
Object.defineProperty(window, "localStorage", {
  value: memoryStorage,
  configurable: true,
});

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => {
  cleanup(); // unmount any leftover React trees from the previous test
  server.resetHandlers();
  memoryStorage.clear();
});
afterAll(() => server.close());
