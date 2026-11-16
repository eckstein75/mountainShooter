import pygame
from pathlib import Path


class Entity:
    def __init__(self, name: str, position: tuple):
        self.name = name

        image_path = (
            Path(__file__).resolve().parent.parent
            / "asset"
            / f"{name}.png"
        )

        self.surf = pygame.image.load(str(image_path)).convert_alpha()

        self.rect = self.surf.get_rect(
            left=position[0],
            top=position[1]
        )

    def move(self):
        pass