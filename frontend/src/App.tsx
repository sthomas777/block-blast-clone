import Grid from "./components/Grid";
import Scoreboard from "./components/Scoreboard";

const MOCK_GRID: number[][] = Array(8).fill(null).map(() => Array(8).fill(0));
// Add some test blocks
MOCK_GRID[2][3] = 3;
MOCK_GRID[2][4] = 3;
MOCK_GRID[3][3] = 3;
MOCK_GRID[3][4] = 3;

function App() {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "20px" }}>
      <h1>Block Blast</h1>
      <Scoreboard score={250}/>
      <Grid grid={MOCK_GRID} />
    </div>
  );
}

export default App
