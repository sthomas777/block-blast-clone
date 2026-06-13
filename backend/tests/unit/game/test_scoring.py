from src.game.scoring import ScoringEngine


def test_init() -> None:
    scoring = ScoringEngine()
    assert scoring.score == 0


def test_add_lines_cleared() -> None:
    scoring = ScoringEngine()
    points = scoring.add_lines_cleared(1)
    assert points == 10
    assert scoring.score == 10


def test_add_multiple_lines() -> None:
    scoring = ScoringEngine()
    scoring.add_lines_cleared(2)
    scoring.add_lines_cleared(3)
    assert scoring.score == 50


def test_get_score() -> None:
    scoring = ScoringEngine()
    scoring.add_lines_cleared(2)
    assert scoring.get_score() == 20


def test_reset() -> None:
    scoring = ScoringEngine()
    scoring.add_lines_cleared(5)
    scoring.reset()
    assert scoring.score == 0
