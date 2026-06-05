import { useState } from "react";
import { useDrag } from "./useDrag";
import type { Coord } from "../types/game";

/**
 * Wires up native HTML drag-and-drop for a single shape preview.
 * Takes the shape's canonical `coordinates` directly — no need to round-trip
 * through a 0/1 matrix and back.
 */
export function useShapeDrag(coordinates: Coord[], shapeIndex: number) {
  const { setCoords } = useDrag();
  const [isDragging, setIsDragging] = useState(false);
  const [dragPos, setDragPos] = useState({ x: 0, y: 0 });

  const createTransparentDragImage = (e: React.DragEvent) => {
    // Hide the browser's default drag ghost; we render our own DragOverlay.
    const emptyImage = new Image();
    e.dataTransfer.setDragImage(emptyImage, 0, 0);
  };

  const handleDragStart = (e: React.DragEvent) => {
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("shapeIndex", shapeIndex.toString());
    e.dataTransfer.setData("shapeCoords", JSON.stringify(coordinates));

    setCoords(coordinates);
    createTransparentDragImage(e);
    setDragPos({ x: e.clientX, y: e.clientY });
    setIsDragging(true);
  };

  const handleDrag = (e: React.DragEvent) => {
    // The final dragend event reports (0,0); ignore it so the overlay
    // doesn't jump to the corner.
    if (e.clientX !== 0 || e.clientY !== 0) {
      setDragPos({ x: e.clientX, y: e.clientY });
    }
  };

  const handleDragEnd = () => {
    setIsDragging(false);
    setCoords(null);
  };

  return { isDragging, dragPos, handleDragStart, handleDrag, handleDragEnd };
}
