import { createContext, useContext, useState, ReactNode } from "react";

interface DragContextType {
  coords: [number, number][] | null;
  setCoords: (coords: [number, number][] | null) => void;
}

const DragContext = createContext<DragContextType | null>(null);

export function DragProvider({ children }: { children: ReactNode }) {
  const [coords, setCoords] = useState<[number, number][] | null>(null);
  return (
    <DragContext.Provider value={{ coords, setCoords }}>
      {children}
    </DragContext.Provider>
  );
}

export function useDrag() {
  const context = useContext(DragContext);
  if (!context) throw new Error("useDrag must be used within DragProvider");
  return context;
}
