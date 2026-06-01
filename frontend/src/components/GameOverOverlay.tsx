interface GameOverProps {
  score: number;
  onNewGame: () => void;
}

export default function GameOverOverlay({ score, onNewGame }: GameOverProps) {
  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0, 0, 0, 0.7)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
    >
      <div
        style={{
          backgroundColor: "#fff",
          padding: "40px",
          borderRadius: "12px",
          textAlign: "center",
          boxShadow: "0 4px 20px rgba(0, 0, 0, 0.3)",
        }}
      >
        <h2 style={{ fontSize: "32px", marginBottom: "20px", color: "#333" }}>
          Game Over
        </h2>
        <p style={{ fontSize: "24px", marginBottom: "30px", color: "#666" }}>
          Final Score: <span style={{ fontWeight: "bold", color: "#2196F3" }}>{score}</span>
        </p>
        <button
          onClick={onNewGame}
          style={{
            padding: "12px 32px",
            fontSize: "16px",
            backgroundColor: "#2196F3",
            color: "#fff",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontWeight: "bold",
            transition: "background-color 0.3s",
          }}
          onMouseEnter={(e) => {
            (e.target as HTMLButtonElement).style.backgroundColor = "#1976D2";
          }}
          onMouseLeave={(e) => {
            (e.target as HTMLButtonElement).style.backgroundColor = "#2196F3";
          }}
        >
          Play Again
        </button>
      </div>
    </div>
  );
}
