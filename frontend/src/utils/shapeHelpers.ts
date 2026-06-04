import type { BlockBlastShape } from "../types/game";

export function calculatePreviewCells(
  row: number,
  col: number,
  shapes: (BlockBlastShape | null)[],
  shapeIndex: number | null,
): number[][] {
  if (shapeIndex === null) return [];
  const shape = shapes[shapeIndex];
  if (!shape) return [];
  return shape.coordinates.map(([r, c]) => [row + r, col + c]);
}

export function getShapeMaxDimensions(shape: number[][]): {
  maxRow: number;
  maxCol: number;
} {
  let maxRow = 0;
  let maxCol = 0;

  for (const row of shape) {
    for (let i = 0; i < row.length; i++) {
      if (row[i] === 1) {
        maxRow = Math.max(maxRow, shape.indexOf(row));
        maxCol = Math.max(maxCol, i);
      }
    }
  }

  return { maxRow, maxCol };
}

export function coordinatesToGrid(coordinates: [number, number][]): number[][] {
  if (coordinates.length === 0) return [];

  const maxRow = Math.max(...coordinates.map(([r]) => r), 0);
  const maxCol = Math.max(...coordinates.map(([, c]) => c), 0);

  const grid: number[][] = Array(maxRow + 1)
    .fill(null)
    .map(() => Array(maxCol + 1).fill(0));

  coordinates.forEach(([r, c]) => {
    grid[r][c] = 1;
  });

  return grid;
}
