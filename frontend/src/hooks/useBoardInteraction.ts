import { useState } from "react";
import type { Coord, GameStateResponse, Position } from "../types/game";
import { calculatePreviewCells } from "../utils/shapeHelpers";

type PlaceBlock = (
  blockIndex: number,
  row: number,
  col: number,
) => Promise<void>;

/**
 * Encapsulates all "board interaction" state and behavior: which shape is
 * selected, where the pointer is hovering, the resulting preview cells, and
 * the click/drop placement handlers.
 *
 * Keeping this in a hook (rather than in a component) makes the logic
 * reusable and testable, and keeps GameBoard focused on layout.
 */
export function useBoardInteraction(
  gameState: GameStateResponse,
  placeBlock: PlaceBlock,
) {
  const [selectedBlock, setSelectedBlock] = useState<number | null>(null);
  const [hoverPos, setHoverPos] = useState<Position | null>(null);

  const handleCellClick = async (row: number, col: number) => {
    if (selectedBlock === null || gameState.game_over) return;
    await placeBlock(selectedBlock, row, col);
    setSelectedBlock(null);
  };

  const handleDrop = async (row: number, col: number, shapeIndex: number) => {
    if (gameState.game_over) return;
    await placeBlock(shapeIndex, row, col);
  };

  // Derived value: no need to store it in state — it's a pure function of
  // hover position + selection + current shapes, recomputed each render.
  const previewCells: Coord[] =
    hoverPos && selectedBlock !== null
      ? calculatePreviewCells(
          hoverPos.row,
          hoverPos.col,
          gameState.shape,
          selectedBlock,
        )
      : [];

  return {
    selectedBlock,
    setSelectedBlock,
    setHoverPos,
    previewCells,
    handleCellClick,
    handleDrop,
  };
}
