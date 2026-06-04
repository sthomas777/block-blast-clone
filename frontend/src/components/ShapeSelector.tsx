import type { BlockBlastShape } from "../types/game.ts";
import ShapePreview from "./ShapePreview";
import { coordinatesToGrid } from "../utils/shapeHelpers";

interface ShapeSelectorProps {
  shapes: (BlockBlastShape | null)[];
  selectedIndex: number | null;
  onSelect: (index: number) => void;
}

function ShapeSelector({
  shapes,
  selectedIndex,
  onSelect,
}: ShapeSelectorProps) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-around",
        alignItems: "center",
        gap: "20px",
        width: "100%",
        minHeight: "100px",
        padding: "10px",
        backgroundColor: "#1a1a1a",
        borderRadius: "12px",
        border: "2px solid #333",
        marginBottom: "24px",
        boxSizing: "border-box",
      }}
    >
      {shapes.map((shape, idx) => {
        if (!shape) return null;

        return (
          <ShapePreview
            key={`${shape.name}-${idx}`}
            shape={coordinatesToGrid(shape.coordinates)}
            color={shape.color}
            isSelected={selectedIndex === idx}
            onShapeClick={() => onSelect(idx)}
            shapeIndex={idx}
          />
        );
      })}
    </div>
  );
}

export default ShapeSelector;
