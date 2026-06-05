// Backend game-state contract + shared domain types.

/** Possible server-side game states (mirrors the backend GameState enum). */
export type GameState =
  | "START"
  | "PLAYER_TURN"
  | "SHAPE_PREVIEW"
  | "LINES_CLEARED"
  | "CHECKING_BOARD"
  | "GAME_OVER";

/**
 * A single [row, col] coordinate. Naming this tuple makes every signature
 * that passes positions around self-documenting and type-checked.
 */
export type Coord = [number, number];

/** A position on the board, used for hover/click handlers. */
export interface Position {
  row: number;
  col: number;
}

/**
 * A shape rendered as a dense matrix of 0/1 (1 = filled cell).
 * Used only for *rendering* a shape preview; the canonical representation
 * coming from the backend is `Coord[]` (see BlockBlastShape.coordinates).
 */
export type ShapeMatrix = number[][];

/** A board cell: 0/"0" means empty, a color string means filled. */
export type CellValue = number | string;

export interface BlockBlastShape {
  name: string;
  coordinates: Coord[];
  color: string;
}

export interface GameStateResponse {
  game_id: string;
  grid: CellValue[][];
  score: number;
  shape: BlockBlastShape[];
  status: GameState;
  game_over: boolean;
}
