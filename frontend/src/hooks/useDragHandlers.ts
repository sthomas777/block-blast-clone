import { useState } from "react";
import { useDrag } from "./useDrag";
import { calculateDropPosition } from "./useDragPreview";
import { isLeavingGrid, parseShapeCoords } from "../utils/gridHelpers";
import type { Position } from "../types/game";

export function useDragHandlers(
  onDrop?: (row: number, col: number, shapeIndex: number) => void,
) {
  const { coords: dragShapeCoords, setCoords } = useDrag();
  const [dragOverCell, setDragOverCell] = useState<Position | null>(null);

  const handleDragOver = (e: React.DragEvent, row: number, col: number) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
    setDragOverCell({ row, col });
  };

  const handleDragLeave = (e: React.DragEvent) => {
    if (isLeavingGrid(e)) {
      setDragOverCell(null);
    }
  };

  const handleDragEnter = (e: React.DragEvent) => {
    const coords = parseShapeCoords(e.dataTransfer);
    if (coords) {
      setCoords(coords);
    }
  };

  const handleDrop = (e: React.DragEvent, row: number, col: number) => {
    e.preventDefault();
    e.stopPropagation();

    const shapeIndexStr = e.dataTransfer.getData("shapeIndex");
    if (!shapeIndexStr || !dragShapeCoords) return;

    const shapeIndex = parseInt(shapeIndexStr, 10);
    const dropPos = calculateDropPosition(row, col, dragShapeCoords);
    onDrop?.(dropPos.row, dropPos.col, shapeIndex);

    setDragOverCell(null);
    setCoords(null);
  };

  return {
    dragOverCell,
    dragShapeCoords,
    handleDragOver,
    handleDragLeave,
    handleDragEnter,
    handleDrop,
  };
}
