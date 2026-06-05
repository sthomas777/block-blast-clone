import { BLOCK_COLORS } from "../utils/colors";
import { BOARD_CELL_SIZE } from "../constants";
import type { CellValue } from "../types/game";
import styles from "../styles/Cell.module.css";

interface CellProps {
  value: CellValue;
  onCellClick?: () => void;
  previewColor?: string;
}

function isEmptyCell(value: CellValue): boolean {
  return value === 0 || value === "0";
}

function getFilledColor(value: CellValue): string {
  return typeof value === "string"
    ? value
    : BLOCK_COLORS[value] || BLOCK_COLORS[0];
}

function Cell({ value, onCellClick, previewColor }: CellProps) {
  const isEmpty = isEmptyCell(value);
  const className = `${styles.cell} ${isEmpty ? styles.empty : styles.filled}`;

  // Background is data-driven, so it stays inline:
  //  - preview highlight wins when present
  //  - filled cells use their own color
  //  - empty cells get no inline bg, so CSS (including :hover) applies
  const backgroundColor =
    previewColor ?? (isEmpty ? undefined : getFilledColor(value));

  return (
    <div
      onClick={onCellClick}
      className={className}
      style={{
        width: `${BOARD_CELL_SIZE}px`,
        height: `${BOARD_CELL_SIZE}px`,
        ...(backgroundColor ? { backgroundColor } : {}),
      }}
    />
  );
}

export default Cell;
