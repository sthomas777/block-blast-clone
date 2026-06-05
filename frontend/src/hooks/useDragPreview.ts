import { GRID_SIZE } from "../constants";
import type { Coord, Position } from "../types/game";

interface ShapeBounds {
  minRow: number;
  maxRow: number;
  minCol: number;
  maxCol: number;
}

interface CenterOffset {
  row: number;
  col: number;
}

function getShapeBounds(coords: Coord[]): ShapeBounds {
  const minRow = Math.min(...coords.map(([r]) => r));
  const maxRow = Math.max(...coords.map(([r]) => r));
  const minCol = Math.min(...coords.map(([, c]) => c));
  const maxCol = Math.max(...coords.map(([, c]) => c));

  return { minRow, maxRow, minCol, maxCol };
}

function getCenterOffset(bounds: ShapeBounds): CenterOffset {
  return {
    row: Math.floor((bounds.maxRow - bounds.minRow) / 2),
    col: Math.floor((bounds.maxCol - bounds.minCol) / 2),
  };
}

export function calculateDragShapeCells(
  dragOverCell: Position | null,
  coords: Coord[] | null,
): Set<string> {
  const cells = new Set<string>();

  if (!dragOverCell || !coords) return cells;

  const bounds = getShapeBounds(coords);
  const centerOffset = getCenterOffset(bounds);

  const anchorRow = dragOverCell.row - bounds.minRow - centerOffset.row;
  const anchorCol = dragOverCell.col - bounds.minCol - centerOffset.col;

  for (const [dr, dc] of coords) {
    const r = anchorRow + dr;
    const c = anchorCol + dc;
    cells.add(`${r}-${c}`);
  }

  return cells;
}

export function calculateDropPosition(
  rowIdx: number,
  colIdx: number,
  coords: Coord[],
  gridSize = GRID_SIZE,
): Position {
  const bounds = getShapeBounds(coords);
  const centerOffset = getCenterOffset(bounds);

  let anchorRow = rowIdx - bounds.minRow - centerOffset.row;
  let anchorCol = colIdx - bounds.minCol - centerOffset.col;

  // Clamp to grid boundaries
  anchorRow = Math.max(0, Math.min(anchorRow, gridSize - 1 - bounds.maxRow));
  anchorCol = Math.max(0, Math.min(anchorCol, gridSize - 1 - bounds.maxCol));

  return { row: anchorRow, col: anchorCol };
}
