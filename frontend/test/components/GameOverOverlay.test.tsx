import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import GameOverOverlay from "../../src/components/GameOverOverlay";

describe("<GameOverOverlay />", () => {
  it("renders the final score", () => {
    render(<GameOverOverlay score={420} onNewGame={vi.fn()} />);
    expect(screen.getByText(/final score/i)).toBeInTheDocument();
    expect(screen.getByText("420")).toBeInTheDocument();
  });

  it("calls onNewGame when 'Play Again' is clicked", async () => {
    const onNewGame = vi.fn();
    const user = userEvent.setup();

    render(<GameOverOverlay score={0} onNewGame={onNewGame} />);
    await user.click(screen.getByRole("button", { name: /play again/i }));

    expect(onNewGame).toHaveBeenCalledOnce();
  });
});
