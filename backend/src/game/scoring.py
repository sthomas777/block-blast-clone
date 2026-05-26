from dataclasses import dataclass


@dataclass
class ScoringEngine:
    score: int = 0

    def add_lines_cleared(self, lines_cleared: int) -> int:
        points = lines_cleared * 10
        self.score += points
        return points

    def get_score(self) -> int:
        return self.score

    def reset(self) -> None:
        self.score = 0
