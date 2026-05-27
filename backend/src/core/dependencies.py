from backend.src.services.game_service import GameService

game_service = GameService()


def get_game_service() -> GameService:
    return game_service
