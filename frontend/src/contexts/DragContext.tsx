import { createContext, useState, type ReactNode } from "react";
import type { Coord } from "../types/game";

interface DragContextType {
  coords: Coord[] | null;
  setCoords: (coords: Coord[] | null) => void;
}

// eslint-disable-next-line react-refresh/only-export-components
export const DragContext = createContext<DragContextType | null>(null);

export function DragProvider({ children }: { children: ReactNode }) {
  const [coords, setCoords] = useState<Coord[] | null>(null);
  return (
    <DragContext.Provider value={{ coords, setCoords }}>
      {children}
    </DragContext.Provider>
  );
}
