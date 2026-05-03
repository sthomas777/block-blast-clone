def calculate_score(lines_cleared: int) -> int:
    return sum(s * 10 for s in range(1, lines_cleared + 1))
