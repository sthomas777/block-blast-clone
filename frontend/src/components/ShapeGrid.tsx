import type { ShapeMatrix } from "../types/game";

interface ShapeGridProps {
  shape: ShapeMatrix;
  color: string;
  cellSize: number;
  gap: number;
  maxRow: number;
  maxCol: number;
}

function ShapeGrid({ shape, color, cellSize, gap, maxCol }: ShapeGridProps) {
  return (
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
  );
}

export default ShapeGrid;
