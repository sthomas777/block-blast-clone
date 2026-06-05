import Grid from "./Grid";
import Scoreboard from "./Scoreboard";
import ShapeSelector from "./ShapeSelector";
import { useBoardInteraction } from "../hooks/useBoardInteraction";
import type { GameStateResponse } from "../types/game";

interface GameBoardProps {
  gameState: GameStateResponse;
  placeBlock: (blockIndex: number, row: number, col: number) => Promise<void>;
}

function GameBoard({ gameState, placeBlock }: GameBoardProps) {
  const {
    selectedBlock,
    setSelectedBlock,
    setHoverPos,
    previewCells,
    handleCellClick,
    handleDrop,
  } = useBoardInteraction(gameState, placeBlock);

  return (
    <>
      <Scoreboard score={gameState.score} />
      <ShapeSelector
        shapes={gameState.shape}
        selectedIndex={gameState.game_over ? null : selectedBlock}
        onSelect={gameState.game_over ? () => {} : setSelectedBlock}
      />
      <Grid
        grid={gameState.grid}
        onCellClick={handleCellClick}
        onCellHover={setHoverPos}
        onDrop={handleDrop}
        previewCells={previewCells}
      />
    </>
  );
}

export default GameBoard;
