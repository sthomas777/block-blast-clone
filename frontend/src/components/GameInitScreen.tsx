import GameControls from "./GameControls";

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
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#1a1a1a",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
        fontFamily: "system-ui, -apple-system, sans-serif",
      }}
    >
      <GameControls
        onNewGame={onCreateGame}
        isLoading={isLoading}
        error={error}
      />
    </div>
  );
}

export default GameInitScreen;
