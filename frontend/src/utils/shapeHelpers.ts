import type { BlockBlastShape, Coord, ShapeMatrix } from "../types/game";

/**
 * Cells the currently-selected shape would occupy if its top-left were
 * placed at (row, col). Returns coordinates in board space.
 */
export function calculatePreviewCells(
  row: number,
  col: number,
  shapes: (BlockBlastShape | null)[],
  shapeIndex: number | null,
): Coord[] {
  if (shapeIndex === null) return [];
  const shape = shapes[shapeIndex];
  if (!shape) return [];
  return shape.coordinates.map(([r, c]) => [row + r, col + c]);
}

/**
 * The largest row/col index occupied by a filled cell in a shape matrix.
 * Used to size the preview grid. Uses the loop indices directly rather
 * than re-searching the array (the old `indexOf` approach was O(n^2)).
 */
export function getShapeMaxDimensions(shape: ShapeMatrix): {
  maxRow: number;
  maxCol: number;
} {
  let maxRow = 0;
  let maxCol = 0;

  shape.forEach((row, r) => {
    row.forEach((cell, c) => {
      if (cell === 1) {
        maxRow = Math.max(maxRow, r);
        maxCol = Math.max(maxCol, c);
      }
    });
  });

  return { maxRow, maxCol };
}

/** Convert a list of filled coordinates into a dense 0/1 matrix for rendering. */
export function coordinatesToGrid(coordinates: Coord[]): ShapeMatrix {
  if (coordinates.length === 0) return [];

  const maxRow = Math.max(...coordinates.map(([r]) => r), 0);
  const maxCol = Math.max(...coordinates.map(([, c]) => c), 0);

  const grid: ShapeMatrix = Array.from({ length: maxRow + 1 }, () =>
    Array.from({ length: maxCol + 1 }, () => 0),
  );

  for (const [r, c] of coordinates) {
    grid[r][c] = 1;
  }

  return grid;
}
