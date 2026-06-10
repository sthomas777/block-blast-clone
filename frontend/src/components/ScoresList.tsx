import type { Score } from "../types/auth";
import styles from "../styles/ScoresList.module.css";

interface ScoresListProps {
  scores: Score[];
}

function ScoresList({ scores }: ScoresListProps) {
  return (
    <div className={styles.panel}>
      <h2 className={styles.title}>My Scores</h2>
      {scores.length === 0 ? (
        <p className={styles.empty}>No scores yet — finish a game!</p>
      ) : (
        <ol className={styles.list}>
          {scores.map((score) => (
            <li key={score.score_id} className={styles.item}>
              <span className={styles.score}>{score.score}</span>
              <span className={styles.lines}>{score.lines_cleared} lines</span>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}

export default ScoresList;
