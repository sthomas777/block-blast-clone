import { describe, expect, it } from "vitest";

import { isLeavingGrid, parseShapeCoords } from "../../src/utils/gridHelpers";

describe("parseShapeCoords", () => {
  function fakeDataTransfer(payload: string | null): DataTransfer {
    return {
      getData: (key: string) => (key === "shapeCoords" ? (payload ?? "") : ""),
    } as unknown as DataTransfer;
  }

  it("returns null when the dataTransfer has no payload", () => {
    expect(parseShapeCoords(fakeDataTransfer(null))).toBeNull();
  });

  it("parses a valid Coord[] JSON payload", () => {
    const dt = fakeDataTransfer(
      JSON.stringify([
        [0, 0],
        [0, 1],
        [1, 0],
      ]),
    );
    expect(parseShapeCoords(dt)).toEqual([
      [0, 0],
      [0, 1],
      [1, 0],
    ]);
  });

  it("returns null on malformed JSON", () => {
    expect(parseShapeCoords(fakeDataTransfer("{not-json"))).toBeNull();
  });

  it("returns null when the payload is not a Coord[]", () => {
    expect(parseShapeCoords(fakeDataTransfer(JSON.stringify({})))).toBeNull();
    expect(
      parseShapeCoords(fakeDataTransfer(JSON.stringify([["a", "b"]]))),
    ).toBeNull();
    expect(
      parseShapeCoords(fakeDataTransfer(JSON.stringify([[1]]))),
    ).toBeNull();
  });
});

describe("isLeavingGrid", () => {
  it("is true when there is no relatedTarget", () => {
    const e = {
      relatedTarget: null,
      currentTarget: document.createElement("div"),
    };
    expect(isLeavingGrid(e as unknown as React.DragEvent)).toBe(true);
  });

  it("is true when relatedTarget is outside the currentTarget", () => {
    const grid = document.createElement("div");
    const outside = document.createElement("div");
    const e = { relatedTarget: outside, currentTarget: grid };
    expect(isLeavingGrid(e as unknown as React.DragEvent)).toBe(true);
  });

  it("is false when relatedTarget is inside the currentTarget", () => {
    const grid = document.createElement("div");
    const child = document.createElement("span");
    grid.appendChild(child);
    const e = { relatedTarget: child, currentTarget: grid };
    expect(isLeavingGrid(e as unknown as React.DragEvent)).toBe(false);
  });
});
