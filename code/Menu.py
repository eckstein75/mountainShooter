import pygame
from pathlib import Path


class Menu:
    def __init__(self, window):
        self.window = window

        image_path = (
            Path(__file__).resolve().parent.parent
            / "asset"
            / "MenuBg.png"
        )

        self.surf = pygame.image.load(str(image_path)).convert()
        self.surf = pygame.transform.scale(
            self.surf, self.window.get_size()
        )

        self.options = ["1 PLAYER", "2 PLAYERS", "EXIT"]
        self.selected = 0

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.window.blit(self.surf, (0, 0))

            width, height = self.window.get_size()

            font_title = pygame.font.Font(None, 45)
            font_menu = pygame.font.Font(None, 31)

            title = font_title.render(
                "MOUNTAIN SHOOTER", True, (255, 255, 255)
            )

            title_rect = title.get_rect(
                center=(width // 2, 48)
            )

            self.window.blit(title, title_rect)

            for index, option in enumerate(self.options):
                color = (
                    (255, 255, 0)
                    if index == self.selected
                    else (255, 255, 255)
                )

                text = font_menu.render(option, True, color)

                text_rect = text.get_rect(
                    center=(
                        width // 2,
                        110 + index * 36
                    )
                )

                self.window.blit(text, text_rect)

            # Instrucoes obrigatorias na tela inicial
            panel = pygame.Surface(
                (width - 24, 106),
                pygame.SRCALPHA
            )
            panel.fill((0, 0, 0, 190))
            self.window.blit(panel, (12, height - 112))

            font_help = pygame.font.Font(None, 21)

            instructions = (
                "J1: W A S D = MOVER | ESPACO = ATIRAR",
                "J2: SETAS = MOVER | CTRL DIREITO = ATIRAR",
                "MENU: SETAS = SELECIONAR | ENTER = INICIAR",
                "DURANTE JOGO: ESC = VOLTAR AO MENU"
            )

            for index, instruction in enumerate(instructions):
                text_help = font_help.render(
                    instruction,
                    True,
                    (255, 255, 255)
                )

                text_help_rect = text_help.get_rect(
                    center=(
                        width // 2,
                        height - 94 + index * 25
                    )
                )

                self.window.blit(text_help, text_help_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "EXIT"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (
                            self.selected - 1
                        ) % len(self.options)

                    elif event.key == pygame.K_DOWN:
                        self.selected = (
                            self.selected + 1
                        ) % len(self.options)

                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selected]

            pygame.display.flip()
            clock.tick(60)