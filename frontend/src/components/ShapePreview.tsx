import { useMemo } from "react";
import ShapeGrid from "./ShapeGrid";
import DragOverlay from "./DragOverlay";
import {
  coordinatesToGrid,
  getShapeMaxDimensions,
} from "../utils/shapeHelpers";
import { useShapeDrag } from "../hooks/useShapeDrag";
import { PREVIEW_CELL_SIZE, PREVIEW_GAP } from "../constants";
import type { Coord } from "../types/game";
import styles from "../styles/ShapePreview.module.css";

interface ShapePreviewProps {
  coordinates: Coord[];
  color: string;
  isSelected: boolean;
  onShapeClick: () => void;
  shapeIndex: number;
}

function ShapePreview({
  coordinates,
  color,
  isSelected,
  onShapeClick,
  shapeIndex,
}: ShapePreviewProps) {
  const { isDragging, dragPos, handleDragStart, handleDrag, handleDragEnd } =
    useShapeDrag(coordinates, shapeIndex);

  // Derive the render matrix from coordinates. useMemo keeps the same array
  // instance between renders unless `coordinates` changes, avoiding needless
  // recomputation.
  const matrix = useMemo(() => coordinatesToGrid(coordinates), [coordinates]);
  const { maxRow, maxCol } = getShapeMaxDimensions(matrix);

  const className = [
    styles.preview,
    isSelected ? styles.selected : "",
    isDragging ? styles.dragging : "",
  ].join(" ");

  return (
    <>
      <div
        draggable
        onClick={onShapeClick}
        onDragStart={handleDragStart}
        onDrag={handleDrag}
        onDragEnd={handleDragEnd}
        className={className}
      >
        <ShapeGrid
          shape={matrix}
          color={color}
          cellSize={PREVIEW_CELL_SIZE}
          gap={PREVIEW_GAP}
          maxRow={maxRow}
          maxCol={maxCol}
        />
      </div>

      {isDragging && (
        <DragOverlay
          shape={matrix}
          color={color}
          dragPos={dragPos}
          maxRow={maxRow}
          maxCol={maxCol}
        />
      )}
    </>
  );
}

export default ShapePreview;
