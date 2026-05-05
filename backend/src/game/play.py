from backend.src.game.session import GameSession


def display_board(session: GameSession) -> None:
    grid = session.get_board_grid()
    print("\n" + "=" * (session.board.cols * 2 + 1))
    for row in grid:
        print(" | " + " ".join(" # " if cell else " · " for cell in row) + " | ")
    print("=" * (session.board.cols * 2 + 1))
    print(f"Score: {session.get_score()}")


def display_shapes(session: GameSession) -> None:
    shapes = session.get_available_shapes()
    print("\nAvailable shapes:")
    for i, shape in enumerate(shapes):
        print(f"{i}:")
        max_row = max(r for r, c in shape.coordinates)
        max_col = max(c for r, c in shape.coordinates)
        for r in range(max_row + 1):
            for c in range(max_col + 1):
                print(" # " if (r, c) in shape.coordinates else " · ", end=" ")
            print()


def get_shape_input(session: GameSession) -> int:
    while True:
        try:
            choice = int(input("Select shape (0-2): "))
            if 0 <= choice < len(session.get_available_shapes()):
                return choice
            print("Invalid choice")
        except ValueError:
            print("Enter a number")


def get_position_input() -> tuple[int, int]:
    while True:
        try:
            row = int(input("Row (0-7): "))
            col = int(input("Col (0-7): "))
            if 0 <= row < 8 and 0 <= col < 8:
                return (row, col)
            print("Out of bounds")
        except ValueError:
            print("Enter numbers")


def play():
    session = GameSession(board_size=(8, 8))
    session.start()

    while not session.is_game_over():
        display_board(session)
        display_shapes(session)

        shape_idx = get_shape_input(session)
        shape = session.get_available_shapes()[shape_idx]

        row, col = get_position_input()
        
        if not session.preview_shape(shape, (row, col)):
            print("Invalid placement!")
            continue
        
        session.confirm_placement()

    display_board(session)
    print(f"\nGame Over! Final Score: {session.get_score()}")


if __name__ == "__main__":
    play()
