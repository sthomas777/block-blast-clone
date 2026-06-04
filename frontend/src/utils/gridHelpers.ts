export function isLeavingGrid(e: React.DragEvent): boolean {
  const relatedTarget = e.relatedTarget as HTMLElement;
  return !relatedTarget || !e.currentTarget.contains(relatedTarget);
}

export function parseShapeCoords(
  dataTransfer: DataTransfer,
): [number, number][] | null {
  const coordsData = dataTransfer.getData("shapeCoords");
  if (!coordsData) return null;

  try {
    return JSON.parse(coordsData);
  } catch {
    return null;
  }
}
