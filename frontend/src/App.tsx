import { useState } from "react";
import { type GameStateResponse, type BlockBlastShape, GameState as GameStateEnum } from "./types/game";
import Grid from "./components/Grid";
import Scoreboard from "./components/Scoreboard";
import ShapeSelector from "./components/ShapeSelector";
import GameOverOverlay from "./components/GameOverOverlay";

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
      
      const isGridFull = newGrid.every(row => row.every(cell => cell !== 0));
      
      return {
        ...prev,
        grid: newGrid,
        shape: newShapes,
        status: isGridFull ? GameStateEnum.GAME_OVER : prev.status,
        game_over: isGridFull,
      } as GameStateResponse;
    });
    setSelectedBlock(null);
  };

  const handleDrop = (row: number, col: number, shapeIndex: number) => {
    // Try exact position first
    let validRow = row;
    let validCol = col;
    let found = false;

    if (isValidPlacement(row, col, shapeIndex)) {
      found = true;
    } else {
      // Check nearby positions (tolerance of 1 cell)
      for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
          if (isValidPlacement(row + dr, col + dc, shapeIndex)) {
            validRow = row + dr;
            validCol = col + dc;
            found = true;
            break;
          }
        }
        if (found) break;
      }
    }

    if (!found) {
      setError("Invalid placement!");
      setTimeout(() => setError(null), 1000);
      return;
    }

    setGameState(prev => {
      const newGrid = prev.grid.map(r => [...r]);
      const shape = prev.shape[shapeIndex];
      const color = parseInt(shape.color) || 1;
      
      for (const [r, c] of shape.coordinates) {
        newGrid[validRow + r][validCol + c] = color;
      }
      
      const newShapes = [...prev.shape] as (BlockBlastShape | null)[];
      newShapes[shapeIndex] = null;
      
      const isGridFull = newGrid.every(row => row.every(cell => cell !== 0));
      
      return {
        ...prev,
        grid: newGrid,
        shape: newShapes,
        status: isGridFull ? GameStateEnum.GAME_OVER : prev.status,
        game_over: isGridFull,
      } as GameStateResponse;
    });
  };

  const handleNewGame = () => {
    setGameState({
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
    setSelectedBlock(null);
    setError(null);
  };

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#1a1a1a",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "20px",
      fontFamily: "system-ui, -apple-system, sans-serif",
    }}>
      <h1 style={{ color: "#fff", fontSize: "48px", marginBottom: "30px", textShadow: "0 2px 8px rgba(0,0,0,0.5)" }}>
        Block Blast
      </h1>
      <div style={{ backgroundColor: "#2a2a2a", padding: "30px", borderRadius: "16px", boxShadow: "0 8px 32px rgba(0,0,0,0.5)" }}>
        <Scoreboard score={gameState.score} />
        <ShapeSelector 
          shapes={gameState.shape} 
          selectedIndex={selectedBlock}
          onSelect={setSelectedBlock}
        />
        {error && (
          <div style={{
            color: "#ff6b6b",
            marginTop: "15px",
            fontWeight: "bold",
            textAlign: "center",
            animation: "shake 0.3s",
          }}>
            {error}
          </div>
        )}
        <Grid 
          grid={gameState.grid} 
          onCellClick={handleCellClick}
          onCellHover={setHoverPos}
          onDrop={handleDrop}
          previewCells={hoverPos && selectedBlock !== null ? getPreviewCells(hoverPos.row, hoverPos.col, selectedBlock) : []}
          isValidPreview={hoverPos && selectedBlock !== null ? isValidPlacement(hoverPos.row, hoverPos.col, selectedBlock) : false}
        />
      </div>
      {gameState.status === GameStateEnum.GAME_OVER && (
        <GameOverOverlay score={gameState.score} onNewGame={handleNewGame} />
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
  );
}

export default App;
