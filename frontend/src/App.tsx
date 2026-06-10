import { useEffect } from "react";

import { useGameState } from "./hooks/useGameState";
import { useAuth } from "./hooks/useAuth";
import { useMyScores } from "./hooks/useMyScores";
import GameBoard from "./components/GameBoard";
import GameOverOverlay from "./components/GameOverOverlay";
import GameInitScreen from "./components/GameInitScreen";
import GameControls from "./components/GameControls";
import AuthForm from "./components/AuthForm";
import UserBar from "./components/UserBar";
import ScoresList from "./components/ScoresList";
import { DragProvider } from "./contexts/DragContext";
import styles from "./styles/App.module.css";

function App() {
  const {
    token,
    player,
    error: authError,
    login,
    register,
    logout,
  } = useAuth();
  const { gameState, error, isConnected, createGame, placeBlock } =
    useGameState(token);
  const { scores, refresh } = useMyScores(token);

  // Refresh the score list when a game ends while signed in.
  const gameOver = gameState?.game_over ?? false;
  useEffect(() => {
    if (gameOver && token) refresh();
  }, [gameOver, token, refresh]);

  const account = player ? (
    <UserBar username={player.username} onLogout={logout} />
  ) : (
    <AuthForm onLogin={login} onRegister={register} error={authError} />
  );

  if (!gameState) {
    return (
      <div className={styles.container}>
        <header className={styles.header}>{account}</header>
        <GameInitScreen
          onCreateGame={createGame}
          isLoading={!isConnected}
          error={error}
        />
      </div>
    );
  }

  return (
    <DragProvider>
      <div className={styles.container}>
        <header className={styles.header}>{account}</header>
        <h1 className={styles.title}>Block Blast</h1>
        {!isConnected && (
          <p className={styles.connecting}>Connecting to server…</p>
        )}
        <div className={styles.gameLayout}>
          <div className={styles.gameContainer}>
            <GameControls
              onNewGame={createGame}
              isLoading={!isConnected}
              error={error}
            />
            <GameBoard gameState={gameState} placeBlock={placeBlock} />
          </div>
          {player && <ScoresList scores={scores} />}
        </div>
        {gameState.game_over && (
          <GameOverOverlay score={gameState.score} onNewGame={createGame} />
        )}
      </div>
    </DragProvider>
  );
}

export default App;
