from code.Background import Background
from code.Enemy import Enemy
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position: tuple = (0, 0)):

        if entity_name.startswith("Level") and "Bg" in entity_name:
            return Background(entity_name, position)

        elif entity_name in ("MenuBg", "ScoreBg"):
            return Background(entity_name, position)

        elif entity_name in ("Player1", "Player2"):
            return Player(entity_name, position)

        elif entity_name in ("Enemy1", "Enemy2"):
            return Enemy(entity_name, position)

        else:
            raise ValueError(
                f"Entidade desconhecida: {entity_name}"
            )