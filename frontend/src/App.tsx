import { useState } from "react";
import { type GameStateResponse, type BlockBlastShape, GameState as GameStateEnum } from "./types/game";
import Grid from "./components/Grid";
import Scoreboard from "./components/Scoreboard";
import ShapeSelector from "./components/ShapeSelector";

function App() {
  const [selectedBlock, setSelectedBlock] = useState<number | null>(null);
  const [hoverPos, setHoverPos] = useState<{ row: number; col: number } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [gameState, setGameState] = useState<GameStateResponse>({
    game_id: "mock-001",
    grid: Array(8).fill(null).map(() => Array(8).fill(0)),
    score: 0,
    shape: [
      { name: "O", coordinates: [[0,0],[0,1],[1,0],[1,1]], color: "1" },
      { name: "I", coordinates: [[0,0],[1,0],[2,0]], color: "2" },
      { name: "L", coordinates: [[0,0],[0,1],[0,2]], color: "3" },
    ],
    status: GameStateEnum.PLAYER_TURN,
    game_over: false,
  });

  const isValidPlacement = (row: number, col: number, shapeIdx: number | null) => {
    if (shapeIdx === null) return false;
    const shape = gameState.shape[shapeIdx];
    if (!shape) return false;
    
    for (const [r, c] of shape.coordinates) {
      const newRow = row + r;
      const newCol = col + c;
      if (newRow < 0 || newRow >= 8 || newCol < 0 || newCol >= 8) return false;
      if (gameState.grid[newRow][newCol] !== 0) return false;
    }
    return true;
  };

  const getPreviewCells = (row: number, col: number, shapeIdx: number | null) => {
    if (shapeIdx === null) return [];
    const shape = gameState.shape[shapeIdx];
    if (!shape) return [];
    return shape.coordinates.map(([r, c]) => [row + r, col + c]);
  };

  const handleCellClick = (row: number, col: number) => {
    if (selectedBlock === null) return;
    
    if (!isValidPlacement(row, col, selectedBlock)) {
      setError("Invalid placement!");
      setTimeout(() => setError(null), 1000);
      return;
    }

    setGameState(prev => {
      const newGrid = prev.grid.map(r => [...r]);
      const shape = prev.shape[selectedBlock];
      const color = parseInt(shape.color) || 1;
      
      for (const [r, c] of shape.coordinates) {
        newGrid[row + r][col + c] = color;
      }
      
      const newShapes = [...prev.shape] as (BlockBlastShape | null)[];
      newShapes[selectedBlock] = null;
      
      return { ...prev, grid: newGrid, shape: newShapes } as GameStateResponse;
    });
    setSelectedBlock(null);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "20px" }}>
      <h1>Block Blast</h1>
      <Scoreboard score={gameState.score} />
      <ShapeSelector 
        shapes={gameState.shape} 
        selectedIndex={selectedBlock}
        onSelect={setSelectedBlock}
      />
      {error && (
        <div style={{
          color: "#ff4444",
          marginTop: "10px",
          fontWeight: "bold",
          animation: "shake 0.3s",
        }}>
          {error}
        </div>
      )}
      <Grid 
        grid={gameState.grid} 
        onCellClick={handleCellClick}
        onCellHover={setHoverPos}
        previewCells={hoverPos && selectedBlock !== null ? getPreviewCells(hoverPos.row, hoverPos.col, selectedBlock) : []}
        isValidPreview={hoverPos && selectedBlock !== null ? isValidPlacement(hoverPos.row, hoverPos.col, selectedBlock) : false}
      />
      <style>{`
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
      `}</style>
    </div>
  );
}

export default App;
