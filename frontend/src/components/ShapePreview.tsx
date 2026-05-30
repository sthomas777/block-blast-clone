import { BLOCK_COLORS } from "../utils/colors";

interface ShapePreviewProps {
  shape: number[][];
  color: number;
  isSelected: boolean;
  onShapeClick: () => void;
}

function ShapePreview({ shape, color, isSelected, onShapeClick }: ShapePreviewProps) {
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

  const cellSize = 20;
  const gap = 1;

  return (
    <div
      onClick={onShapeClick}
      style={{
        padding: "8px",
        border: isSelected ? "2px solid #fff" : "2px solid transparent",
        borderRadius: "4px",
        cursor: "pointer",
        display: "inline-block",
        backgroundColor: isSelected ? "rgba(255, 255, 255, 0.1)" : "transparent",
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
                backgroundColor: cell === 1 ? BLOCK_COLORS[color] : "transparent",
                borderRadius: "2px",
              }}
            />
          ))
        )}
      </div>
    </div>
  );
}

export default ShapePreview;
