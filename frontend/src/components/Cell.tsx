import { BLOCK_COLORS } from "../utils/colors";

interface CellProps {
  value: number;
  onCellClick?: () => void;
}

function Cell({ value, onCellClick }: CellProps) {
  return (
    <div
      onClick={onCellClick}
      style={{
        backgroundColor: BLOCK_COLORS[value] || BLOCK_COLORS[0],
        width: "40px",
        height: "40px",
        borderRadius: "4px",
        cursor: "pointer",
      }}
    />
  );
}

export default Cell;
