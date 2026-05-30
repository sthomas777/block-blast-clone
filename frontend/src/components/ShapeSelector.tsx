import type { BlockBlastShape } from "../types/game.ts";
import ShapePreview from "./ShapePreview";

interface ShapeSelectorProps {
  shapes: (BlockBlastShape | null)[];
  selectedIndex: number | null;
  onSelect: (index: number) => void;
}

function ShapeSelector({ shapes, selectedIndex, onSelect }: ShapeSelectorProps) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px", width: "300px", minHeight: "100px", justifyItems: "center" }}>
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
          />
        ) : (
          <div key={idx} />
        )
      )}
    </div>
  );
}

export default ShapeSelector;
