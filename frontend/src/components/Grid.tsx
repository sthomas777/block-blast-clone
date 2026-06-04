import Cell from "./Cell";
import { calculateDragShapeCells } from "../hooks/useDragPreview";
import { useDragHandlers } from "../hooks/useDragHandlers";

interface GridProps {
  grid: (number | string)[][];
  onCellClick?: (row: number, col: number) => void;
  onCellHover?: (pos: { row: number; col: number } | null) => void;
  onDrop?: (row: number, col: number, shapeIndex: number) => void;
  previewCells?: number[][];
}

function Grid({
  grid,
  onCellClick,
  onCellHover,
  onDrop,
  previewCells = [],
}: GridProps) {
  const {
    dragOverCell,
    dragShapeCoords,
    handleDragOver,
    handleDragLeave,
    handleDragEnter,
    handleDrop,
  } = useDragHandlers(onDrop);

  const previewSet = new Set(previewCells.map(([r, c]) => `${r}-${c}`));
  const dragShapeCells = calculateDragShapeCells(dragOverCell, dragShapeCoords);

  const getCellStyle = (isDragShape: boolean): React.CSSProperties => ({
    opacity: isDragShape ? 0.8 : 1,
    outline: isDragShape ? "2px solid yellow" : "none",
    outlineOffset: "-2px",
  });

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(8, 50px)",
        gap: "8px",
        padding: "20px",
        backgroundColor: "#1a1a1a",
        borderRadius: "12px",
        boxShadow:
          "inset 0 4px 12px rgba(0,0,0,0.8), 0 8px 24px rgba(0,0,0,0.5)",
      }}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
    >
      {grid.map((row, rowIdx) =>
        row.map((value, colIdx) => {
          const isPreview = previewSet.has(`${rowIdx}-${colIdx}`);
          const isDragShape = dragShapeCells.has(`${rowIdx}-${colIdx}`);

          return (
            <div
              key={`${rowIdx}-${colIdx}`}
              onMouseEnter={() => onCellHover?.({ row: rowIdx, col: colIdx })}
              onMouseLeave={() => onCellHover?.(null)}
              onDragOver={(e) => handleDragOver(e, rowIdx, colIdx)}
              onDrop={(e) => handleDrop(e, rowIdx, colIdx)}
              style={getCellStyle(isDragShape)}
            >
              <Cell
                value={value}
                onCellClick={() => onCellClick?.(rowIdx, colIdx)}
                previewColor={
                  isPreview ? "rgba(100, 200, 255, 0.5)" : undefined
                }
              />
            </div>
          );
        }),
      )}
    </div>
  );
}

export default Grid;
