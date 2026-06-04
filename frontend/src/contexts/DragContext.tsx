import { createContext, useState, type ReactNode } from "react";

interface DragContextType {
  coords: [number, number][] | null;
  setCoords: (coords: [number, number][] | null) => void;
}

// eslint-disable-next-line react-refresh/only-export-components
export const DragContext = createContext<DragContextType | null>(null);

export function DragProvider({ children }: { children: ReactNode }) {
  const [coords, setCoords] = useState<[number, number][] | null>(null);
  return (
    <DragContext.Provider value={{ coords, setCoords }}>
      {children}
    </DragContext.Provider>
  );
}
