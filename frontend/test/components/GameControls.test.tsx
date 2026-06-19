import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import GameControls from "../../src/components/GameControls";

describe("<GameControls />", () => {
  it("renders the New Game button enabled when not loading", () => {
    render(<GameControls onNewGame={vi.fn()} isLoading={false} error={null} />);
    const button = screen.getByRole("button", { name: /new game/i });
    expect(button).toBeEnabled();
  });

  it("disables the button and shows 'Creating...' while loading", () => {
    render(<GameControls onNewGame={vi.fn()} isLoading={true} error={null} />);
    const button = screen.getByRole("button", { name: /creating/i });
    expect(button).toBeDisabled();
  });

  it("calls onNewGame when the button is clicked", async () => {
    const onNewGame = vi.fn();
    const user = userEvent.setup();

    render(
      <GameControls onNewGame={onNewGame} isLoading={false} error={null} />,
    );
    await user.click(screen.getByRole("button", { name: /new game/i }));

    expect(onNewGame).toHaveBeenCalledOnce();
  });

  it("renders the error message when one is provided", () => {
    render(
      <GameControls
        onNewGame={vi.fn()}
        isLoading={false}
        error="Connection lost"
      />,
    );
    expect(screen.getByText("Connection lost")).toBeInTheDocument();
  });

  it("does not render an error block when error is null", () => {
    const { container } = render(
      <GameControls onNewGame={vi.fn()} isLoading={false} error={null} />,
    );
    expect(container.querySelectorAll("div")).toHaveLength(0);
  });
});
