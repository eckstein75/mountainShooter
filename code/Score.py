from pathlib import Path

import pygame

from code.ScoreProxy import ScoreProxy


class Score:
    def __init__(self, window, score, game_mode, level_name="Level1"):
        self.window = window
        self.score = int(score)
        self.game_mode = game_mode
        self.level_name = level_name
        self.player_name = ""
        self.saved = False
        self.save_error = ""
        self.clock = pygame.time.Clock()
        self.proxy = ScoreProxy()

        asset_dir = Path(__file__).resolve().parent.parent / "asset"

        background = pygame.image.load(
            str(asset_dir / "ScoreBg.png")
        ).convert()

        self.background = pygame.transform.scale(
            background,
            self.window.get_size()
        )

        self.font_title = pygame.font.Font(None, 42)
        self.font_text = pygame.font.Font(None, 26)
        self.font_small = pygame.font.Font(None, 23)

    def draw(self):
        self.window.blit(self.background, (0, 0))

        width, height = self.window.get_size()

        overlay = pygame.Surface(
            (width, height),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 140))
        self.window.blit(overlay, (0, 0))

        title = self.font_title.render(
            "MOUNTAIN SHOOTER - SCORE",
            True,
            (255, 215, 0)
        )

        self.window.blit(
            title,
            title.get_rect(center=(width // 2, 30))
        )

        final_score = self.font_text.render(
            f"PONTUACAO: {self.score}",
            True,
            (255, 255, 255)
        )

        self.window.blit(
            final_score,
            final_score.get_rect(center=(width // 2, 75))
        )

        label = (
            "JOGADOR" if self.game_mode == "1 PLAYER"
            else "DUPLA"
        )

        if self.save_error:
            name_text = f"AVISO: {self.save_error[:30]}"
        elif self.saved:
            name_text = f"SALVO: {self.player_name}"
        else:
            name_text = f"{label}: {self.player_name}_"

        name_surface = self.font_small.render(
            name_text, True, (255, 255, 255)
        )

        self.window.blit(
            name_surface,
            name_surface.get_rect(center=(width // 2, 105))
        )

        ranking_title = self.font_text.render(
            "TOP 5 - MELHORES PONTUACOES",
            True,
            (255, 215, 0)
        )

        self.window.blit(
            ranking_title,
            ranking_title.get_rect(center=(width // 2, 136))
        )

        ranking = self.proxy.best_scores(limit=5)

        if not ranking:
            message = self.font_small.render(
                "Nenhuma pontuacao registrada",
                True,
                (255, 255, 255)
            )

            self.window.blit(
                message,
                message.get_rect(center=(width // 2, 160))
            )

        for index, item in enumerate(ranking, start=1):
            name = str(item["player_name"])[:14]

            text = self.font_small.render(
                f"{index}. {name} - {item['score']} pontos",
                True,
                (255, 255, 255)
            )

            self.window.blit(
                text,
                text.get_rect(
                    center=(width // 2, 144 + index * 24)
                )
            )

        instruction = self.font_small.render(
            ("ENTER: MENU | ESC: MENU" if self.saved
             else "DIGITE O NOME - ENTER: SALVAR"),
            True,
            (255, 215, 0)
        )

        self.window.blit(
            instruction,
            instruction.get_rect(
                center=(width // 2, height - 17)
            )
        )

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "EXIT"

                if event.type != pygame.KEYDOWN:
                    continue

                if self.saved:
                    if event.key in (
                        pygame.K_RETURN, pygame.K_ESCAPE
                    ):
                        return "MENU"

                elif event.key == pygame.K_ESCAPE:
                    return "MENU"

                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                    self.save_error = ""

                elif event.key == pygame.K_RETURN:
                    name = self.player_name.strip()

                    if not name:
                        self.save_error = "DIGITE UM NOME"
                        continue

                    try:
                        self.proxy.save(
                            self.score,
                            self.game_mode,
                            self.level_name,
                            name
                        )

                    except Exception as error:
                        self.save_error = "FALHA AO SALVAR"
                        print(f"ERRO AO SALVAR SCORE: {error}")

                    else:
                        self.player_name = name
                        self.saved = True
                        self.save_error = ""
                        print("SCORE SALVO COM SUCESSO")

                elif len(self.player_name) < 16:
                    char = getattr(event, "unicode", "")

                    if char and char.isprintable():
                        self.player_name = (
                            self.player_name + char
                        )[:16]
                        self.save_error = ""

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
