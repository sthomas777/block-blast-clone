import Grid from "./Grid";
import Scoreboard from "./Scoreboard";
import ShapeSelector from "./ShapeSelector";
import type { GameStateResponse } from "../types/game";

interface GameBoardProps {
  gameState: GameStateResponse;
  selectedBlock: number | null;
  onSelectBlock: (index: number) => void;
  onCellClick: (row: number, col: number) => void;
  onCellHover: (pos: { row: number; col: number } | null) => void;
  onDrop: (row: number, col: number, shapeIndex: number) => void;
  previewCells: number[][];
}

function GameBoard({
  gameState,
  selectedBlock,
  onSelectBlock,
  onCellClick,
  onCellHover,
  onDrop,
  previewCells,
}: GameBoardProps) {
  return (
    <>
      <Scoreboard score={gameState.score} />
      <ShapeSelector
        shapes={gameState.shape}
        selectedIndex={gameState.game_over ? null : selectedBlock}
        onSelect={gameState.game_over ? () => {} : onSelectBlock}
      />
      <Grid
        grid={gameState.grid}
        onCellClick={onCellClick}
        onCellHover={onCellHover}
        onDrop={onDrop}
        previewCells={previewCells}
      />
    </>
  );
}

export default GameBoard;
