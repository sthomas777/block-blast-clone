export const GameState = {
START: "START",
PLAYER_TURN: "PLAYER_TURN",
SHAPE_PREVIEW: "SHAPE_PREVIEW",
LINES_CLEARED: "LINES_CLEARED",
CHECKING_BOARD: "CHECKING_BOARD",
GAME_OVER: "GAME_OVER",
} as const;

export type GameState = typeof GameState[keyof typeof GameState];


export interface BlockBlastShape {
  name: string;
  coordinates: [number, number][];
  color: string;
}

export interface GameStateResponse {
  game_id: string;
  grid: number[][];
  score: number;
  shape: BlockBlastShape[];
  status: GameState;
  game_over: boolean;
}
