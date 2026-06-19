import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import type { Score } from "../../src/types/auth";
import ScoresList from "../../src/components/ScoresList";

const SCORES: Score[] = [
  {
    score_id: 1,
    player_id: 1,
    session_id: null,
    score: 300,
    lines_cleared: 30,
    achieved_at: "2026-01-01T00:00:00Z",
  },
  {
    score_id: 2,
    player_id: 1,
    session_id: null,
    score: 100,
    lines_cleared: 10,
    achieved_at: "2026-01-02T00:00:00Z",
  },
];

describe("<ScoresList />", () => {
  it("always renders the heading", () => {
    render(<ScoresList scores={[]} />);
    expect(
      screen.getByRole("heading", { name: /my scores/i }),
    ).toBeInTheDocument();
  });

  it("shows the empty-state message when there are no scores", () => {
    render(<ScoresList scores={[]} />);
    expect(screen.getByText(/no scores yet/i)).toBeInTheDocument();
    expect(screen.queryByRole("list")).toBeNull();
  });

  it("renders each score and its lines-cleared label", () => {
    render(<ScoresList scores={SCORES} />);

    const list = screen.getByRole("list");
    const items = within(list).getAllByRole("listitem");
    expect(items).toHaveLength(2);

    expect(within(items[0]).getByText("300")).toBeInTheDocument();
    expect(within(items[0]).getByText("30 lines")).toBeInTheDocument();
    expect(within(items[1]).getByText("100")).toBeInTheDocument();
    expect(within(items[1]).getByText("10 lines")).toBeInTheDocument();
  });

  it("does not render the empty-state message when scores exist", () => {
    render(<ScoresList scores={SCORES} />);
    expect(screen.queryByText(/no scores yet/i)).toBeNull();
  });
});
