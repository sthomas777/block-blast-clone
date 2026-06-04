import ShapeGrid from "./ShapeGrid";
import DragOverlay from "./DragOverlay";
import { getShapeMaxDimensions } from "../utils/shapeHelpers";
import { useShapeDrag } from "../hooks/useShapeDrag";

interface ShapePreviewProps {
  shape: number[][];
  color: string;
  isSelected: boolean;
  onShapeClick: () => void;
  shapeIndex: number;
}

const PREVIEW_CELL_SIZE = 16;
const PREVIEW_GAP = 1;

function ShapePreview({
  shape,
  color,
  isSelected,
  shapeIndex,
}: ShapePreviewProps) {
  const { isDragging, dragPos, handleDragStart, handleDrag, handleDragEnd } =
    useShapeDrag(shape, shapeIndex);

  const { maxRow, maxCol } = getShapeMaxDimensions(shape);

  return (
    <>
      <div
        draggable
        onDragStart={handleDragStart}
        onDrag={handleDrag}
        onDragEnd={handleDragEnd}
        style={{
          padding: "6px",
          border: isSelected ? "3px solid #4fc3f7" : "none",
          borderRadius: "8px",
          cursor: "grab",
          display: "inline-block",
          opacity: isDragging ? 0 : 1,
          backgroundColor: isSelected
            ? "rgba(79, 195, 247, 0.15)"
            : "rgba(255, 255, 255, 0.05)",
          transition: "all 0.2s ease",
          boxShadow: isSelected ? "0 0 12px rgba(79, 195, 247, 0.3)" : "none",
          userSelect: "none",
        }}
      >
        <ShapeGrid
          shape={shape}
          color={color}
          cellSize={PREVIEW_CELL_SIZE}
          gap={PREVIEW_GAP}
          maxRow={maxRow}
          maxCol={maxCol}
        />
      </div>

      {isDragging && (
        <DragOverlay
          shape={shape}
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
