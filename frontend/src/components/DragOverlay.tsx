import ShapeGrid from "./ShapeGrid";

interface DragOverlayProps {
  shape: number[][];
  color: string;
  dragPos: { x: number; y: number };
  maxRow: number;
  maxCol: number;
}

function DragOverlay({
  shape,
  color,
  dragPos,
  maxRow,
  maxCol,
}: DragOverlayProps) {
  const cellSize = 50;
  const gap = 8;

  return (
    <div
      style={{
        position: "fixed",
        left: `${dragPos.x - ((maxCol + 1) * cellSize) / 2 - (gap * maxCol) / 2}px`,
        top: `${dragPos.y - ((maxRow + 1) * cellSize) / 2 - (gap * maxRow) / 2}px`,
        pointerEvents: "none",
        zIndex: 10000,
        padding: "6px",
        backgroundColor: "rgba(79, 195, 247, 0.2)",
        borderRadius: "8px",
        border: "2px solid #4fc3f7",
      }}
    >
      <ShapeGrid
        shape={shape}
        color={color}
        cellSize={cellSize}
        gap={gap}
        maxRow={maxRow}
        maxCol={maxCol}
      />
    </div>
  );
}

export default DragOverlay;
