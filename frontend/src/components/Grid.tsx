import Cell from "./Cell";

interface GridProps {
  grid: number[][];
}

function Grid({ grid }: GridProps) {
  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(8, 40px)",
      gap: "2px",
    }}>
      {grid.flat().map((value, index) => (
        <Cell key={index} value={value} />
      ))}
    </div>
  );
}

export default Grid;
