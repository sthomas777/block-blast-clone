import { BLOCK_COLORS } from "../utils/colors";

interface CellProps {
  value: number | string;
  onCellClick?: () => void;
  previewColor?: string;
}

function getCellColor(value: number | string, previewColor?: string): string {
  if (previewColor) return previewColor;

  return typeof value === "string"
    ? value
    : BLOCK_COLORS[value] || BLOCK_COLORS[0];
}

function isEmptyCell(value: number | string): boolean {
  return value === 0 || value === "0";
}

function handleCellHover(
  e: React.MouseEvent<HTMLDivElement>,
  value: number | string,
  originalBgColor: string,
  isEnter: boolean,
) {
  if (!isEmptyCell(value)) return;

  (e.currentTarget as HTMLDivElement).style.backgroundColor = isEnter
    ? "#333"
    : originalBgColor;
}

function Cell({ value, onCellClick, previewColor }: CellProps) {
  const bgColor = getCellColor(value, previewColor);
  const isEmpty = isEmptyCell(value);

  return (
    <div
      onClick={onCellClick}
      style={{
        backgroundColor: bgColor,
        width: "50px",
        height: "50px",
        borderRadius: "8px",
        cursor: "pointer",
        boxShadow: isEmpty
          ? "inset 0 2px 4px rgba(0,0,0,0.3)"
          : "0 4px 8px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.1)",
        transition: "all 0.2s ease",
        border: "1px solid rgba(255,255,255,0.05)",
      }}
      onMouseEnter={(e) => handleCellHover(e, value, bgColor, true)}
      onMouseLeave={(e) => handleCellHover(e, value, bgColor, false)}
    />
  );
}

export default Cell;
