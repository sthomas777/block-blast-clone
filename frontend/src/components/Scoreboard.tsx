import styles from "../styles/Scoreboard.module.css";

interface ScoreboardProps {
  score: number;
}

function Scoreboard({ score }: ScoreboardProps) {
  return (
    <div className={styles.scoreboard}>
      <h2 className={styles.heading}>
        Score: <span className={styles.value}>{score}</span>
      </h2>
    </div>
  );
}

export default Scoreboard;
