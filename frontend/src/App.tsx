import { useState } from "react";
import { useGameApi } from "./hooks/useGameApi";
import Grid from "./components/Grid";
import Scoreboard from "./components/Scoreboard";
import ShapeSelector from "./components/ShapeSelector";
import GameOverOverlay from "./components/GameOverOverlay";
import { DragProvider } from "./contexts/DragContext";

function App() {
  const { gameState, isLoading, error, createGame, placeBlock } = useGameApi();
  const [selectedBlock, setSelectedBlock] = useState<number | null>(null);
  const [hoverPos, setHoverPos] = useState<{ row: number; col: number } | null>(
    null,
  );

  if (!gameState) {
    return (
      <div
        style={{
          minHeight: "100vh",
          backgroundColor: "#1a1a1a",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "20px",
          fontFamily: "system-ui, -apple-system, sans-serif",
        }}
      >
        <button
          onClick={createGame}
          disabled={isLoading}
          style={{
            padding: "10px 20px",
            backgroundColor: "#4CAF50",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            cursor: isLoading ? "not-allowed" : "pointer",
            fontSize: "16px",
            fontWeight: "bold",
          }}
        >
          {isLoading ? "Creating..." : "New Game"}
        </button>
        {error && (
          <p style={{ color: "#ff6b6b", marginTop: "20px" }}>{error}</p>
        )}
      </div>
    );
  }

  const getPreviewCells = (
    row: number,
    col: number,
    shapeIdx: number | null,
  ) => {
    if (shapeIdx === null) return [];
    const shape = gameState.shape[shapeIdx];
    if (!shape) return [];
    return shape.coordinates.map(([r, c]) => [row + r, col + c]);
  };

  const handlePlaceBlock = async (row: number, col: number) => {
    if (selectedBlock === null || gameState.game_over) return;
    await placeBlock(selectedBlock, row, col);
    setSelectedBlock(null);
  };

  const handleDrop = async (row: number, col: number, shapeIndex: number) => {
    if (gameState.game_over) return;
    await placeBlock(shapeIndex, row, col);
  };

  return (
    <DragProvider>
      <div
        style={{
          minHeight: "100vh",
          backgroundColor: "#1a1a1a",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "20px",
          fontFamily: "system-ui, -apple-system, sans-serif",
        }}
      >
        <h1
          style={{
            color: "#fff",
            fontSize: "48px",
            marginBottom: "30px",
            textShadow: "0 2px 8px rgba(0,0,0,0.5)",
          }}
        >
          Block Blast
        </h1>
        <div
          style={{
            backgroundColor: "#2a2a2a",
            padding: "30px",
            borderRadius: "16px",
            boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
          }}
        >
          <button
            onClick={createGame}
            disabled={isLoading}
            style={{
              padding: "10px 20px",
              marginBottom: "20px",
              backgroundColor: "#4CAF50",
              color: "#fff",
              border: "none",
              borderRadius: "8px",
              cursor: isLoading ? "not-allowed" : "pointer",
              fontSize: "16px",
              fontWeight: "bold",
            }}
          >
            {isLoading ? "Creating..." : "New Game"}
          </button>
          {error && (
            <div
              style={{
                color: "#ff6b6b",
                marginTop: "15px",
                fontWeight: "bold",
                textAlign: "center",
              }}
            >
              {error}
            </div>
          )}
          <Scoreboard score={gameState.score} />
          <ShapeSelector
            shapes={gameState.shape}
            selectedIndex={gameState.game_over ? null : selectedBlock}
            onSelect={gameState.game_over ? () => {} : setSelectedBlock}
          />
          <Grid
            grid={gameState.grid}
            onCellClick={handlePlaceBlock}
            onCellHover={setHoverPos}
            onDrop={handleDrop}
            previewCells={
              hoverPos && selectedBlock !== null
                ? getPreviewCells(hoverPos.row, hoverPos.col, selectedBlock)
                : []
            }
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
