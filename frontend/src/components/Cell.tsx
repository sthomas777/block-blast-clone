import { BLOCK_COLORS } from "../utils/colors";

interface CellProps {
  value: number;  // 0=empty, 1-7=color
}

function Cell({ value }: CellProps) {
  return (
    <div
      style={{
        backgroundColor: BLOCK_COLORS[value] || BLOCK_COLORS[0],
        width: "40px",
        height: "40px",
        borderRadius: "4px",
      }}
    />
  );
}

export default Cell;
