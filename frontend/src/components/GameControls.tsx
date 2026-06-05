import styles from "../styles/GameControls.module.css";

interface GameControlsProps {
  onNewGame: () => void;
  isLoading: boolean;
  error: string | null;
}

function GameControls({ onNewGame, isLoading, error }: GameControlsProps) {
  return (
    <>
      <button
        onClick={onNewGame}
        disabled={isLoading}
        className={styles.newGameButton}
      >
        {isLoading ? "Creating..." : "New Game"}
      </button>
      {error && <div className={styles.error}>{error}</div>}
    </>
  );
}

export default GameControls;
