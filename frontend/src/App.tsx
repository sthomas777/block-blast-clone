import { useState } from "react";
import { useGameApi } from "./hooks/useGameApi";
import GameBoard from "./components/GameBoard";
import GameOverOverlay from "./components/GameOverOverlay";
import GameInitScreen from "./components/GameInitScreen";
import GameControls from "./components/GameControls";
import { DragProvider } from "./contexts/DragContext";
import { calculatePreviewCells } from "./utils/shapeHelpers";
import {
  containerStyle,
  titleStyle,
  gameContainerStyle,
} from "./styles/appStyles";

function App() {
  const { gameState, isLoading, error, createGame, placeBlock } = useGameApi();
  const [selectedBlock, setSelectedBlock] = useState<number | null>(null);
  const [hoverPos, setHoverPos] = useState<{ row: number; col: number } | null>(
    null,
  );

  if (!gameState) {
    return (
      <GameInitScreen
        onCreateGame={createGame}
        isLoading={isLoading}
        error={error}
      />
    );
  }

  const handlePlaceBlock = async (row: number, col: number) => {
    if (selectedBlock === null || gameState.game_over) return;
    await placeBlock(selectedBlock, row, col);
    setSelectedBlock(null);
  };

  const handleDrop = async (row: number, col: number, shapeIndex: number) => {
    if (gameState.game_over) return;
    await placeBlock(shapeIndex, row, col);
  };

  const previewCells =
    hoverPos && selectedBlock !== null
      ? calculatePreviewCells(
          hoverPos.row,
          hoverPos.col,
          gameState.shape,
          selectedBlock,
        )
      : [];

  return (
    <DragProvider>
      <div style={containerStyle}>
        <h1 style={titleStyle}>Block Blast</h1>
        <div style={gameContainerStyle}>
          <GameControls
            onNewGame={createGame}
            isLoading={isLoading}
            error={error}
          />
          <GameBoard
            gameState={gameState}
            selectedBlock={selectedBlock}
            onSelectBlock={setSelectedBlock}
            onCellClick={handlePlaceBlock}
            onCellHover={setHoverPos}
            onDrop={handleDrop}
            previewCells={previewCells}
          />
        </div>
        {gameState.game_over && (
          <GameOverOverlay score={gameState.score} onNewGame={createGame} />
        )}
        <style>{`
        body {
          margin: 0;
          background-color: #1a1a1a;
        }
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
      `}</style>
      </div>
    </DragProvider>
  );
}

export default App;
