import { useContext } from "react";
import { DragContext } from "../contexts/DragContext";

export function useDrag() {
  const context = useContext(DragContext);
  if (!context) throw new Error("useDrag must be used within DragProvider");
  return context;
}
