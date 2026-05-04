import pytest
from backend.src.game.scoring import calculate_score


@pytest.mark.parametrize(
    "lines_cleared, expected_score",
    [
        pytest.param(1, 10),
        pytest.param(2, 30),
        pytest.param(3, 60),
    ],
)
def test_calculate_score(lines_cleared: int, expected_score: int) -> None:
    actual = calculate_score(lines_cleared)
    assert actual == expected_score
