import Cell from "./Cell";
import { calculateDragShapeCells } from "../hooks/useDragPreview";
import { useDragHandlers } from "../hooks/useDragHandlers";
import { BOARD_CELL_SIZE, BOARD_GAP, GRID_SIZE } from "../constants";
import type { CellValue, Coord, Position } from "../types/game";
import styles from "../styles/Grid.module.css";

interface GridProps {
  grid: CellValue[][];
  onCellClick?: (row: number, col: number) => void;
  onCellHover?: (pos: Position | null) => void;
  onDrop?: (row: number, col: number, shapeIndex: number) => void;
  previewCells?: Coord[];
}

function Grid({
  grid,
  onCellClick,
  onCellHover,
  onDrop,
  previewCells = [],
}: GridProps) {
  const {
    dragOverCell,
    dragShapeCoords,
    handleDragOver,
    handleDragLeave,
    handleDragEnter,
    handleDrop,
  } = useDragHandlers(onDrop);

  const previewSet = new Set(previewCells.map(([r, c]) => `${r}-${c}`));
  const dragShapeCells = calculateDragShapeCells(dragOverCell, dragShapeCoords);

  return (
    <div
      className={styles.board}
      // Grid template + gap are derived from JS constants, so they stay inline.
      style={{
        gridTemplateColumns: `repeat(${GRID_SIZE}, ${BOARD_CELL_SIZE}px)`,
        gap: `${BOARD_GAP}px`,
      }}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
    >
      {grid.map((row, rowIdx) =>
        row.map((value, colIdx) => {
          const isPreview = previewSet.has(`${rowIdx}-${colIdx}`);
          const isDragShape = dragShapeCells.has(`${rowIdx}-${colIdx}`);

          return (
            <div
              key={`${rowIdx}-${colIdx}`}
              className={`${styles.cellWrapper} ${isDragShape ? styles.dragShape : ""}`}
              onMouseEnter={() => onCellHover?.({ row: rowIdx, col: colIdx })}
              onMouseLeave={() => onCellHover?.(null)}
              onDragOver={(e) => handleDragOver(e, rowIdx, colIdx)}
              onDrop={(e) => handleDrop(e, rowIdx, colIdx)}
            >
              <Cell
                value={value}
                onCellClick={() => onCellClick?.(rowIdx, colIdx)}
                previewColor={
                  isPreview ? "rgba(100, 200, 255, 0.5)" : undefined
                }
              />
            </div>
          );
        }),
      )}
    </div>
  );
}

export default Grid;
