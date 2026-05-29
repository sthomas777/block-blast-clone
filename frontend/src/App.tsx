import { useState } from "react";
import { type GameStateResponse, GameState as GameStateEnum } from "./types/game";
import Grid from "./components/Grid";
import Scoreboard from "./components/Scoreboard";

function App() {
  const [gameState, setGameState] = useState<GameStateResponse>({
    game_id: "mock-001",
    grid: Array(8).fill(null).map(() => Array(8).fill(0)),
    score: 0,
    shape: [
      { name: "O", coordinates: [[0,0],[0,1],[1,0],[1,1]], color: "#3333ff" },
      { name: "I", coordinates: [[0,0],[1,0],[2,0]], color: "#ff5500" },
      { name: "L", coordinates: [[0,0],[0,1],[0,2]], color: "#00ff00" },
    ],
    status: GameStateEnum.PLAYER_TURN,
    game_over: false,
  });

  const handleCellClick = (row: number, col: number) => {
    setGameState(prev => {
      const newGrid = prev.grid.map(r => [...r]);
      newGrid[row][col] = newGrid[row][col] === 0 ? 3 : 0;
      return { ...prev, grid: newGrid };
    });
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "20px" }}>
      <h1>Block Blast</h1>
      <Scoreboard score={gameState.score} />
      <Grid grid={gameState.grid} onCellClick={handleCellClick} />
    </div>
  );
}

export default App;
