import pytest
from game.board import create_grid, print_grid

def test_create_grid() -> None:
    grid = create_grid()
    assert len(grid) == 8, f"Grid is not 8 rows, Rows: {len(grid)}"
    for row in grid:
        assert len(row) == 8, f"Row: {row} is not length of 8. Length: {len(row)}"
        for col in row:
            assert col == 0, f"Row: {row} Col: {col} is not 0"

def test_print_grid(capsys: pytest.CaptureFixture[str]) -> None:
    grid = create_grid()
    print_grid(grid)
    captured = capsys.readouterr()
    expected_output = ("0 0 0 0 0 0 0 0\n"
                       "0 0 0 0 0 0 0 0\n"
                       "0 0 0 0 0 0 0 0\n"
                       "0 0 0 0 0 0 0 0\n"
                       "0 0 0 0 0 0 0 0\n"
                       "0 0 0 0 0 0 0 0\n"
                       "0 0 0 0 0 0 0 0\n"
                       "0 0 0 0 0 0 0 0\n")

    assert expected_output == captured.out