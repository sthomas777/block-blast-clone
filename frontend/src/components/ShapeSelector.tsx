import type { BlockBlastShape } from "../types/game.ts";
import ShapePreview from "./ShapePreview";
import styles from "../styles/ShapeSelector.module.css";

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
    <div className={styles.selector}>
      {shapes.map((shape, idx) => {
        if (!shape) return null;

        return (
          <ShapePreview
            key={`${shape.name}-${idx}`}
            coordinates={shape.coordinates}
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
