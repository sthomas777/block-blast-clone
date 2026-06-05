import ShapeGrid from "./ShapeGrid";
import { BOARD_CELL_SIZE, BOARD_GAP } from "../constants";
import type { ShapeMatrix } from "../types/game";
import styles from "../styles/DragOverlay.module.css";

interface DragOverlayProps {
  shape: ShapeMatrix;
  color: string;
  dragPos: { x: number; y: number };
  maxRow: number;
  maxCol: number;
}

function DragOverlay({
  shape,
  color,
  dragPos,
  maxRow,
  maxCol,
}: DragOverlayProps) {
  const cellSize = BOARD_CELL_SIZE;
  const gap = BOARD_GAP;

  return (
    <div
      className={styles.overlay}
      // left/top track the live cursor position, so they stay inline.
      style={{
        left: `${dragPos.x - ((maxCol + 1) * cellSize) / 2 - (gap * maxCol) / 2}px`,
        top: `${dragPos.y - ((maxRow + 1) * cellSize) / 2 - (gap * maxRow) / 2}px`,
      }}
    >
      <ShapeGrid
        shape={shape}
        color={color}
        cellSize={cellSize}
        gap={gap}
        maxRow={maxRow}
        maxCol={maxCol}
      />
    </div>
  );
}

export default DragOverlay;
