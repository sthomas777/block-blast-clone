import { useState } from "react";
import { useDrag } from "./useDrag";

export function useShapeDrag(shape: number[][], shapeIndex: number) {
  const { setCoords } = useDrag();
  const [isDragging, setIsDragging] = useState(false);
  const [dragPos, setDragPos] = useState({ x: 0, y: 0 });

  const extractShapeCoordinates = (): [number, number][] => {
    return shape
      .map((row, r) =>
        row.map((cell, c) => (cell === 1 ? [r, c] : null)).filter(Boolean),
      )
      .flat() as [number, number][];
  };

  const createTransparentDragImage = (e: React.DragEvent) => {
    const emptyImage = new Image();
    e.dataTransfer.setDragImage(emptyImage, 0, 0);
  };

  const handleDragStart = (e: React.DragEvent) => {
    const coords = extractShapeCoordinates();

    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("shapeIndex", shapeIndex.toString());
    e.dataTransfer.setData("shapeCoords", JSON.stringify(coords));

    setCoords(coords);
    createTransparentDragImage(e);
    setDragPos({ x: e.clientX, y: e.clientY });
    setIsDragging(true);
  };

  const handleDrag = (e: React.DragEvent) => {
    if (e.clientX !== 0 || e.clientY !== 0) {
      setDragPos({ x: e.clientX, y: e.clientY });
    }
  };

  const handleDragEnd = () => {
    setIsDragging(false);
    setCoords(null);
  };

  return {
    isDragging,
    dragPos,
    handleDragStart,
    handleDrag,
    handleDragEnd,
  };
}
