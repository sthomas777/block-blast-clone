interface ScoreboardProps {
  score: number;
}

function Scoreboard({ score }: ScoreboardProps) {
  return (
    <div>
      <h2>Score: {score}</h2>
    </div>
  );
}

export default Scoreboard;
