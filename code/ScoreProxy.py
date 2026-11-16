from code.ScoreStorage import ScoreStorage


class ScoreProxy:
    """Proxy para validar e controlar o armazenamento."""

    def __init__(self, storage=None):
        self._storage = (
            storage if storage is not None else ScoreStorage
        )

    def save(self, score, game_mode, level_name, player_name):
        if not isinstance(player_name, str):
            raise ValueError("Nome do jogador invalido")

        name = player_name.strip()

        if not 1 <= len(name) <= 16:
            raise ValueError("Nome deve ter de 1 a 16 caracteres")

        if not all(char.isprintable() for char in name):
            raise ValueError("Nome contem caracteres invalidos")

        if (
            isinstance(score, bool)
            or not isinstance(score, int)
            or score < 0
        ):
            raise ValueError("Pontuacao invalida")

        if game_mode not in ("1 PLAYER", "2 PLAYERS"):
            raise ValueError("Modo de jogo invalido")

        if level_name not in ("Level1", "Level2"):
            raise ValueError("Fase invalida")

        return self._storage.save(
            score, game_mode, level_name, name
        )

    def best_scores(self, limit=5):
        if (
            isinstance(limit, bool)
            or not isinstance(limit, int)
            or not 1 <= limit <= 100
        ):
            raise ValueError("Limite de ranking invalido")

        return self._storage.best_scores(limit=limit)
