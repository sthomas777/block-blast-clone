import styles from "../styles/GameOverOverlay.module.css";

interface GameOverProps {
  score: number;
  onNewGame: () => void;
}

export default function GameOverOverlay({ score, onNewGame }: GameOverProps) {
  return (
    <div className={styles.overlay}>
      <div className={styles.dialog}>
        <h2 className={styles.title}>Game Over</h2>
        <p className={styles.score}>
          Final Score: <span className={styles.scoreValue}>{score}</span>
        </p>
        <button onClick={onNewGame} className={styles.button}>
          Play Again
        </button>
      </div>
    </div>
  );
}
