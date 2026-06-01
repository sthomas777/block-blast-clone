import type { BlockBlastShape } from "../types/game.ts";
import ShapePreview from "./ShapePreview";

interface ShapeSelectorProps {
  shapes: (BlockBlastShape | null)[];
  selectedIndex: number | null;
  onSelect: (index: number) => void;
}

function ShapeSelector({ shapes, selectedIndex, onSelect }: ShapeSelectorProps) {
  return (
    <div style={{
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
    }}>
      {shapes.map((shape, idx) =>
        shape ? (
          <ShapePreview
            key={idx}
            shape={shape.coordinates.reduce((grid, [row, col]) => {
              if (!grid[row]) grid[row] = [];
              grid[row][col] = 1;
              return grid;
            }, [] as number[][]) || []}
            color={parseInt(shape.color) || 1}
            isSelected={selectedIndex === idx}
            onShapeClick={() => onSelect(idx)}
            shapeIndex={idx}
          />
        ) : null
      )}
    </div>
  );
}

export default ShapeSelector;
