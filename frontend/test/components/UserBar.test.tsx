import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import UserBar from "../../src/components/UserBar";

describe("<UserBar />", () => {
  it("renders the username inside the greeting", () => {
    render(<UserBar username="test" onLogout={vi.fn()} />);
    expect(screen.getByText(/signed in as/i)).toBeInTheDocument();
    expect(screen.getByText("test")).toBeInTheDocument();
  });

  it("calls onLogout when the log out button is clicked", async () => {
    const onLogout = vi.fn();
    const user = userEvent.setup();

    render(<UserBar username="test" onLogout={onLogout} />);
    await user.click(screen.getByRole("button", { name: /log out/i }));

    expect(onLogout).toHaveBeenCalledOnce();
  });
});
