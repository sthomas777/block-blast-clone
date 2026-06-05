import { useGameState } from "./hooks/useGameState";
import GameBoard from "./components/GameBoard";
import GameOverOverlay from "./components/GameOverOverlay";
import GameInitScreen from "./components/GameInitScreen";
import GameControls from "./components/GameControls";
import { DragProvider } from "./contexts/DragContext";
import styles from "./styles/App.module.css";

function App() {
  const { gameState, error, isConnected, createGame, placeBlock } =
    useGameState();

  if (!gameState) {
    return (
      <GameInitScreen
        onCreateGame={createGame}
        isLoading={!isConnected}
        error={error}
      />
    );
  }

  return (
    <DragProvider>
      <div className={styles.container}>
        <h1 className={styles.title}>Block Blast</h1>
        {!isConnected && (
          <p className={styles.connecting}>Connecting to server…</p>
        )}
        <div className={styles.gameContainer}>
          <GameControls
            onNewGame={createGame}
            isLoading={!isConnected}
            error={error}
          />
          <GameBoard gameState={gameState} placeBlock={placeBlock} />
        </div>
        {gameState.game_over && (
          <GameOverOverlay score={gameState.score} onNewGame={createGame} />
        )}
      </div>
    </DragProvider>
  );
}

export default App;
