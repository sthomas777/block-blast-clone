export type GameState = "START" | "PLAYER_TURN" | "SHAPE_PREVIEW" | "LINES_CLEARED" | "CHECKING_BOARD" | "GAME_OVER";


export interface BlockBlastShape {
  name: string;
  coordinates: [number, number][];
  color: string;
}

export interface GameStateResponse {
  game_id: string;
  grid: (number | string)[][];
  score: number;
  shape: BlockBlastShape[];
  status: GameState;
  game_over: boolean;
}
