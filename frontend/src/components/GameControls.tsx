import { newGameButtonStyle, errorStyle } from "../styles/appStyles";

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
        style={{
          ...newGameButtonStyle,
          cursor: isLoading ? "not-allowed" : "pointer",
        }}
      >
        {isLoading ? "Creating..." : "New Game"}
      </button>
      {error && <div style={errorStyle}>{error}</div>}
    </>
  );
}

export default GameControls;
