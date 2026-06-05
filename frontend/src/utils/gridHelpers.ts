import type { Coord } from "../types/game";

export function isLeavingGrid(e: React.DragEvent): boolean {
  const relatedTarget = e.relatedTarget as HTMLElement;
  return !relatedTarget || !e.currentTarget.contains(relatedTarget);
}

/** Narrow unknown JSON into Coord[] so callers get a real, checked type. */
function isCoordArray(value: unknown): value is Coord[] {
  return (
    Array.isArray(value) &&
    value.every(
      (pair) =>
        Array.isArray(pair) &&
        pair.length === 2 &&
        typeof pair[0] === "number" &&
        typeof pair[1] === "number",
    )
  );
}

export function parseShapeCoords(dataTransfer: DataTransfer): Coord[] | null {
  const coordsData = dataTransfer.getData("shapeCoords");
  if (!coordsData) return null;

  try {
    const parsed: unknown = JSON.parse(coordsData);
    return isCoordArray(parsed) ? parsed : null;
  } catch {
    return null;
  }
}
