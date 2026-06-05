import { useState } from "react";
import useWebSocketImport, { ReadyState } from "react-use-websocket";
import type { GameStateResponse } from "../types/game";

// react-use-websocket ships as CommonJS. Under some bundler interop (notably
// Vite's dev pre-bundling) the default import resolves to the module's
// `exports` object — `{ __esModule, default: <hook>, ReadyState, ... }` —
// rather than the hook function itself. Normalize to the callable hook so it
// works in both dev and production builds.
type UseWebSocketHook = typeof useWebSocketImport;
const useWebSocket: UseWebSocketHook =
  (useWebSocketImport as unknown as { default?: UseWebSocketHook }).default ??
  useWebSocketImport;

const WS_URL = "ws://localhost:8000/ws/game";

/**
 * The two kinds of message the server sends back:
 *  - a bare GameStateResponse on success (no discriminator tag)
 *  - an ErrorResponse tagged with command_type: "error"
 */
interface ServerError {
  command_type: "error";
  code: "validation_error" | "game_error" | "internal_error";
  message: string;
}

function isServerError(msg: unknown): msg is ServerError {
  return (
    typeof msg === "object" &&
    msg !== null &&
    (msg as Record<string, unknown>).command_type === "error"
  );
}

function isGameState(msg: unknown): msg is GameStateResponse {
  return (
    typeof msg === "object" &&
    msg !== null &&
    typeof (msg as Record<string, unknown>).game_id === "string"
  );
}

interface UseGameStateReturn {
  gameState: GameStateResponse | null;
  error: string | null;
  isConnected: boolean;
  createGame: () => Promise<void>;
  placeBlock: (blockIndex: number, row: number, col: number) => Promise<void>;
}

/**
 * Game communication over a single WebSocket connection.
 *
 * Same createGame / placeBlock surface as the previous REST hook (so no
 * components needed to change), but commands go out as WebSocket messages
 * and state updates come from server pushes.
 */
export function useGameState(): UseGameStateReturn {
  const [gameState, setGameState] = useState<GameStateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const { sendJsonMessage, readyState } = useWebSocket(WS_URL, {
    shouldReconnect: () => true,
    reconnectInterval: 3000,
    // Handle each server push in the message callback (not a setState-in-effect).
    // Success messages are bare game state; errors carry command_type: "error".
    // The backend has no ping/pong — uvicorn handles low-level keepalive.
    onMessage: (event: MessageEvent) => {
      let msg: unknown;
      try {
        msg = JSON.parse(event.data as string);
      } catch {
        return;
      }

      if (isServerError(msg)) {
        setError(msg.message);
      } else if (isGameState(msg)) {
        setGameState(msg);
        setError(null);
      }
    },
  });

  const createGame = async () => {
    sendJsonMessage({ command_type: "new_game" });
  };

  const placeBlock = async (blockIndex: number, row: number, col: number) => {
    sendJsonMessage({
      command_type: "place_shape",
      shape_index: blockIndex,
      row,
      col,
    });
  };

  const isConnected = readyState === ReadyState.OPEN;

  return { gameState, error, isConnected, createGame, placeBlock };
}
