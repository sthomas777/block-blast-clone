import { describe, expect, it } from "vitest";

import type { BlockBlastShape } from "../../src/types/game";
import {
  calculatePreviewCells,
  coordinatesToGrid,
  getShapeMaxDimensions,
} from "../../src/utils/shapeHelpers";

const L_SHAPE: BlockBlastShape = {
  name: "L",
  color: "#e74c3c",
  // L-shape: top-left, below, below-right
  coordinates: [
    [0, 0],
    [1, 0],
    [1, 1],
  ],
};

describe("calculatePreviewCells", () => {
  it("offsets every coordinate by the cursor row/col", () => {
    expect(calculatePreviewCells(3, 4, [L_SHAPE], 0)).toEqual([
      [3, 4],
      [4, 4],
      [4, 5],
    ]);
  });

  it("returns [] when no shape is selected", () => {
    expect(calculatePreviewCells(0, 0, [L_SHAPE], null)).toEqual([]);
  });

  it("returns [] when the indexed shape is missing/null", () => {
    expect(calculatePreviewCells(0, 0, [null], 0)).toEqual([]);
  });
});

describe("getShapeMaxDimensions", () => {
  it("returns 0/0 for an empty matrix", () => {
    expect(getShapeMaxDimensions([])).toEqual({ maxRow: 0, maxCol: 0 });
  });

  it("returns the largest filled row/col indices", () => {
    // 2x3 matrix where the bottom-right cell is filled
    const matrix = [
      [1, 0, 0],
      [0, 0, 1],
    ];
    expect(getShapeMaxDimensions(matrix)).toEqual({ maxRow: 1, maxCol: 2 });
  });

  it("ignores empty rows below filled rows", () => {
    const matrix = [
      [1, 0],
      [0, 0],
    ];
    expect(getShapeMaxDimensions(matrix)).toEqual({ maxRow: 0, maxCol: 0 });
  });
});

describe("coordinatesToGrid", () => {
  it("returns [] when given no coordinates", () => {
    expect(coordinatesToGrid([])).toEqual([]);
  });

  it("places filled cells at their coordinates and zero elsewhere", () => {
    expect(coordinatesToGrid(L_SHAPE.coordinates)).toEqual([
      [1, 0],
      [1, 1],
    ]);
  });

  it("sizes the grid to fit the largest coordinate", () => {
    const grid = coordinatesToGrid([
      [0, 0],
      [2, 3],
    ]);
    expect(grid).toHaveLength(3);
    expect(grid[0]).toHaveLength(4);
    expect(grid[0][0]).toBe(1);
    expect(grid[2][3]).toBe(1);
    expect(grid[1][1]).toBe(0);
  });
});
