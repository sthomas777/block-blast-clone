import Cell from "./Cell";

interface GridProps {
  grid: number[][];
  onCellClick?: (row: number, col: number) => void;
  onCellHover?: (pos: { row: number; col: number } | null) => void;
  previewCells?: number[][];
  isValidPreview?: boolean;
}

function Grid({ grid, onCellClick, onCellHover, previewCells = [], isValidPreview = false }: GridProps) {
  const previewSet = new Set(previewCells.map(([r, c]) => `${r}-${c}`));

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(8, 40px)",
      gap: "2px",
    }}>
      {grid.map((row, rowIdx) =>
        row.map((value, colIdx) => {
          const isPreview = previewSet.has(`${rowIdx}-${colIdx}`);
          return (
            <div
              key={`${rowIdx}-${colIdx}`}
              onMouseEnter={() => onCellHover?.({ row: rowIdx, col: colIdx })}
              onMouseLeave={() => onCellHover?.(null)}
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
