interface ScoreboardProps {
  score: number;
}

function Scoreboard({ score }: ScoreboardProps) {
  return (
    <div style={{ marginBottom: "24px", textAlign: "center" }}>
      <h2 style={{ color: "#fff", fontSize: "28px", margin: "0", letterSpacing: "1px" }}>
        Score: <span style={{ color: "#4fc3f7" }}>{score}</span>
      </h2>
    </div>
  );
}

export default Scoreboard;
