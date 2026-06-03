import { useState } from "react";
import { type GameStateResponse } from "../types/game";

const API_BASE = "http://localhost:8000";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

interface UseGameApiReturn {
  gameState: GameStateResponse | null;
  isLoading: boolean;
  error: string | null;
  createGame: () => Promise<void>;
  placeBlock: (blockIndex: number, row: number, col: number) => Promise<void>;
}

export function useGameApi(): UseGameApiReturn {
  const [gameState, setGameState] = useState<GameStateResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createGame = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiFetch<GameStateResponse>("/game/new", {
        method: "POST",
      });
      setGameState(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create game");
    } finally {
      setIsLoading(false);
    }
  };

  const placeBlock = async (blockIndex: number, row: number, col: number) => {
    if (!gameState) return;
    setIsLoading(true);
    setError(null);
    try {
      await apiFetch(`/game/${gameState.game_id}/place`, {
        method: "POST",
        body: JSON.stringify({ shape_index: blockIndex, row, col }),
      });
      const data = await apiFetch<GameStateResponse>(
        `/game/${gameState.game_id}`,
      );
      setGameState(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to place block");
    } finally {
      setIsLoading(false);
    }
  };

  return { gameState, isLoading, error, createGame, placeBlock };
}
