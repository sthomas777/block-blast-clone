import { useState } from "react";
import Cell from "./Cell";

interface GridProps {
  grid: (number | string)[][];
  onCellClick?: (row: number, col: number) => void;
  onCellHover?: (pos: { row: number; col: number } | null) => void;
  onDrop?: (row: number, col: number, shapeIndex: number) => void;
  previewCells?: number[][];
  isValidPreview?: boolean;
}

// Global to track dragging shape across components
let globalDragShapeCoords: [number, number][] | null = null;

export function setGlobalDragShape(_shapeIndex: number, coords: [number, number][]) {
  globalDragShapeCoords = coords;
}

export function clearGlobalDragShape() {
  globalDragShapeCoords = null;
}

function Grid({ grid, onCellClick, onCellHover, onDrop, previewCells = [], isValidPreview = false }: GridProps) {
  const previewSet = new Set(previewCells.map(([r, c]) => `${r}-${c}`));
  const [dragOverCell, setDragOverCell] = useState<{ row: number; col: number } | null>(null);

  const handleDragOver = (e: React.DragEvent, rowIdx: number, colIdx: number) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
    setDragOverCell({ row: rowIdx, col: colIdx });
  };

  const handleDragLeave = (e: React.DragEvent) => {
    // Only clear if leaving the grid entirely, not just moving between cells
    const relatedTarget = e.relatedTarget as HTMLElement;
    if (!relatedTarget || !e.currentTarget.contains(relatedTarget)) {
      setDragOverCell(null);
    }
  };

  const handleDragEnter = (e: React.DragEvent) => {
    const coordsData = e.dataTransfer.getData("shapeCoords");
    if (coordsData) {
      try {
        globalDragShapeCoords = JSON.parse(coordsData);
      } catch {
        // Ignore parse errors
      }
    }
  };

  const handleDrop = (e: React.DragEvent, rowIdx: number, colIdx: number) => {
    e.preventDefault();
    e.stopPropagation();
    const data = e.dataTransfer.getData("shapeIndex");
    if (data && globalDragShapeCoords) {
      const shapeIndex = parseInt(data);
      
      // Calculate shape's center offset
      const minRow = Math.min(...globalDragShapeCoords.map(([r]) => r));
      const maxRow = Math.max(...globalDragShapeCoords.map(([r]) => r));
      const minCol = Math.min(...globalDragShapeCoords.map(([, c]) => c));
      const maxCol = Math.max(...globalDragShapeCoords.map(([, c]) => c));
      
      const centerOffsetRow = Math.floor((maxRow - minRow) / 2);
      const centerOffsetCol = Math.floor((maxCol - minCol) / 2);
      
      // Adjust drop position so shape centers on dropped cell
      const anchorRow = rowIdx - minRow - centerOffsetRow;
      const anchorCol = colIdx - minCol - centerOffsetCol;
      
      onDrop?.(anchorRow, anchorCol, shapeIndex);
    }
    setDragOverCell(null);
    clearGlobalDragShape();
  };

  // Calculate which cells the dragged shape would occupy
  const dragShapeCells = new Set<string>();
  if (dragOverCell && globalDragShapeCoords) {
    // Calculate shape's center offset
    const minRow = Math.min(...globalDragShapeCoords.map(([r]) => r));
    const maxRow = Math.max(...globalDragShapeCoords.map(([r]) => r));
    const minCol = Math.min(...globalDragShapeCoords.map(([, c]) => c));
    const maxCol = Math.max(...globalDragShapeCoords.map(([, c]) => c));
    
    const centerOffsetRow = Math.floor((maxRow - minRow) / 2);
    const centerOffsetCol = Math.floor((maxCol - minCol) / 2);
    
    // Adjust drop position so shape centers on hovered cell
    const anchorRow = dragOverCell.row - minRow - centerOffsetRow;
    const anchorCol = dragOverCell.col - minCol - centerOffsetCol;
    
    for (const [dr, dc] of globalDragShapeCoords) {
      const r = anchorRow + dr;
      const c = anchorCol + dc;
      dragShapeCells.add(`${r}-${c}`);
    }
  }

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(8, 50px)",
      gap: "8px",
      padding: "20px",
      backgroundColor: "#1a1a1a",
      borderRadius: "12px",
      boxShadow: "inset 0 4px 12px rgba(0,0,0,0.8), 0 8px 24px rgba(0,0,0,0.5)",
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
              style={{
                opacity: isDragShape ? 0.8 : 1,
                outline: isDragShape ? "2px solid yellow" : "none",
                outlineOffset: "-2px",
              }}
            >
              <Cell 
                value={value}
                onCellClick={() => onCellClick?.(rowIdx, colIdx)}
                previewColor={isPreview ? (isValidPreview ? "rgba(100, 200, 100, 0.5)" : "rgba(255, 0, 0, 0.5)") : undefined}
              />
            </div>
          );
        })
      )}
    </div>
  );
}

export default Grid;
