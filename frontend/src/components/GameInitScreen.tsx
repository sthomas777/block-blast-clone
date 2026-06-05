import GameControls from "./GameControls";
import styles from "../styles/GameInitScreen.module.css";

interface GameInitScreenProps {
  onCreateGame: () => void;
  isLoading: boolean;
  error: string | null;
}

function GameInitScreen({
  onCreateGame,
  isLoading,
  error,
}: GameInitScreenProps) {
  return (
    <div className={styles.initContainer}>
      <GameControls
        onNewGame={onCreateGame}
        isLoading={isLoading}
        error={error}
      />
    </div>
  );
}

export default GameInitScreen;
