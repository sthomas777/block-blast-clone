import { BLOCK_COLORS } from "../utils/colors";

interface CellProps {
  value: number;
  onCellClick?: () => void;
  previewColor?: string;
}

function Cell({ value, onCellClick, previewColor }: CellProps) {
  return (
    <div
      onClick={onCellClick}
      style={{
        backgroundColor: previewColor || BLOCK_COLORS[value] || BLOCK_COLORS[0],
        width: "40px",
        height: "40px",
        borderRadius: "4px",
        cursor: "pointer",
      }}
    />
  );
}

export default Cell;
