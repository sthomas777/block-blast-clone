// Single source of truth for layout/sizing values used across the UI.
// Changing a value here updates every component that derives from it,
// instead of hunting down hardcoded numbers in multiple files.

/** The board is GRID_SIZE x GRID_SIZE cells. */
export const GRID_SIZE = 8;

/** Size (px) of a cell on the main board. */
export const BOARD_CELL_SIZE = 50;

/** Gap (px) between cells on the main board. */
export const BOARD_GAP = 8;

/** Size (px) of a cell in the small shape previews in the selector. */
export const PREVIEW_CELL_SIZE = 16;

/** Gap (px) between cells in the small shape previews. */
export const PREVIEW_GAP = 1;
