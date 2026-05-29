import Cell from "./Cell";

interface GridProps {
  grid: number[][];
  onCellClick?: (row: number, col: number) => void;
}

function Grid({ grid, onCellClick }: GridProps) {
  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(8, 40px)",
      gap: "2px",
    }}>
      {grid.map((row, rowIdx) =>
        row.map((value, colIdx) => (
          <Cell 
            key={`${rowIdx}-${colIdx}`}
            value={value}
            onCellClick={() => onCellClick?.(rowIdx, colIdx)}
          />
        ))
      )}
    </div>
  );
}

export default Grid;
