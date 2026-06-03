import { useState } from "react";
import { useDrag } from "../contexts/DragContext";

interface ShapePreviewProps {
  shape: number[][];
  color: string;
  isSelected: boolean;
  onShapeClick: () => void;
  shapeIndex: number;
}

function ShapePreview({
  shape,
  color,
  isSelected,
  shapeIndex,
}: ShapePreviewProps) {
  const { setCoords } = useDrag();
  const [isDragging, setIsDragging] = useState(false);
  const [dragPos, setDragPos] = useState({ x: 0, y: 0 });

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

  const cellSize = 16;
  const gap = 1;
  const dragCellSize = 50;
  const dragGap = 8;

  const handleDragStart = (e: React.DragEvent) => {
    const coords = shape
      .map((row, r) =>
        row.map((cell, c) => (cell === 1 ? [r, c] : null)).filter(Boolean),
      )
      .flat() as [number, number][];

    e.dataTransfer!.effectAllowed = "move";
    e.dataTransfer!.setData("shapeIndex", shapeIndex.toString());
    e.dataTransfer!.setData("shapeCoords", JSON.stringify(coords));

    setCoords(coords);

    // Create a transparent drag image to replace the default
    const emptyImage = new Image();
    e.dataTransfer!.setDragImage(emptyImage, 0, 0);

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
        <div
          style={{
            display: "grid",
            gridTemplateColumns: `repeat(${maxCol + 1}, ${cellSize}px)`,
            gap: `${gap}px`,
          }}
        >
          {shape.map((row, rowIdx) =>
            row.map((cell, colIdx) => (
              <div
                key={`${rowIdx}-${colIdx}`}
                style={{
                  width: `${cellSize}px`,
                  height: `${cellSize}px`,
                  backgroundColor: cell === 1 ? color : "transparent",
                  borderRadius: "4px",
                  boxShadow: cell === 1 ? "0 2px 4px rgba(0,0,0,0.3)" : "none",
                }}
              />
            )),
          )}
        </div>
      </div>

      {isDragging && (
        <div
          style={{
            position: "fixed",
            left: `${dragPos.x - ((maxCol + 1) * dragCellSize) / 2 - (dragGap * maxCol) / 2}px`,
            top: `${dragPos.y - ((maxRow + 1) * dragCellSize) / 2 - (dragGap * maxRow) / 2}px`,
            pointerEvents: "none",
            zIndex: 10000,
            padding: "6px",
            backgroundColor: "rgba(79, 195, 247, 0.2)",
            borderRadius: "8px",
            border: "2px solid #4fc3f7",
          }}
        >
          <div
            style={{
              display: "grid",
              gridTemplateColumns: `repeat(${maxCol + 1}, ${dragCellSize}px)`,
              gap: `${dragGap}px`,
            }}
          >
            {shape.map((row, rowIdx) =>
              row.map((cell, colIdx) => (
                <div
                  key={`${rowIdx}-${colIdx}`}
                  style={{
                    width: `${dragCellSize}px`,
                    height: `${dragCellSize}px`,
                    backgroundColor: cell === 1 ? color : "transparent",
                    borderRadius: "4px",
                    boxShadow:
                      cell === 1 ? "0 2px 8px rgba(0,0,0,0.5)" : "none",
                  }}
                />
              )),
            )}
          </div>
        </div>
      )}
    </>
  );
}

export default ShapePreview;
