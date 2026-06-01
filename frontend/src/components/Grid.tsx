import Cell from "./Cell";

interface GridProps {
  grid: number[][];
  onCellClick?: (row: number, col: number) => void;
  onCellHover?: (pos: { row: number; col: number } | null) => void;
  onDrop?: (row: number, col: number, shapeIndex: number, shapeCoords: [number, number][]) => void;
  previewCells?: number[][];
  isValidPreview?: boolean;
}

function Grid({ grid, onCellClick, onCellHover, onDrop, previewCells = [], isValidPreview = false }: GridProps) {
  const previewSet = new Set(previewCells.map(([r, c]) => `${r}-${c}`));

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const data = e.dataTransfer.getData("shapeIndex");
    const coordsData = e.dataTransfer.getData("shapeCoords");
    if (data && coordsData) {
      const shapeIndex = parseInt(data);
      const shapeCoords = JSON.parse(coordsData) as [number, number][];
      const gridContainer = e.currentTarget.closest('[style*="display: grid"]') as HTMLElement;
      if (gridContainer) {
        const rect = gridContainer.getBoundingClientRect();
        const cellSize = 50;
        const gap = 8;
        const x = e.clientX - rect.left - 20;
        const y = e.clientY - rect.top - 20;
        
        // Calculate center of shape
        let maxRow = 0, maxCol = 0;
        for (const [r, c] of shapeCoords) {
          maxRow = Math.max(maxRow, r);
          maxCol = Math.max(maxCol, c);
        }
        const centerRow = maxRow / 2;
        const centerCol = maxCol / 2;
        
        const cursorRow = y / (cellSize + gap);
        const cursorCol = x / (cellSize + gap);
        const adjustedRow = Math.floor(cursorRow - centerRow);
        const adjustedCol = Math.floor(cursorCol - centerCol);
        
        onDrop?.(adjustedRow, adjustedCol, shapeIndex, shapeCoords);
      }
    }
  };

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(8, 50px)",
      gap: "8px",
      padding: "20px",
      backgroundColor: "#1a1a1a",
      borderRadius: "12px",
      boxShadow: "inset 0 4px 12px rgba(0,0,0,0.8), 0 8px 24px rgba(0,0,0,0.5)",
    }}>
      {grid.map((row, rowIdx) =>
        row.map((value, colIdx) => {
          const isPreview = previewSet.has(`${rowIdx}-${colIdx}`);
          return (
            <div
              key={`${rowIdx}-${colIdx}`}
              onMouseEnter={() => onCellHover?.({ row: rowIdx, col: colIdx })}
              onMouseLeave={() => onCellHover?.(null)}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
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
