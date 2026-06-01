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
        width: "50px",
        height: "50px",
        borderRadius: "8px",
        cursor: "pointer",
        boxShadow: value !== 0 ? "0 4px 8px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.1)" : "inset 0 2px 4px rgba(0,0,0,0.3)",
        transition: "all 0.2s ease",
        border: "1px solid rgba(255,255,255,0.05)",
      }}
      onMouseEnter={(e) => {
        if (value === 0) {
          (e.currentTarget as HTMLDivElement).style.backgroundColor = "#333";
        }
      }}
      onMouseLeave={(e) => {
        if (value === 0) {
          (e.currentTarget as HTMLDivElement).style.backgroundColor = BLOCK_COLORS[0];
        }
      }}
    />
  );
}

export default Cell;
