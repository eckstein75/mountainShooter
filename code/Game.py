import pygame
from pathlib import Path

from code.Menu import Menu
from code.Level import Level
from code.Score import Score


class Game:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((576, 324))
        pygame.display.set_caption("Mountain Shooter")


    def play_music(self, filename):
        if not pygame.mixer.get_init():
            return

        music_path = (
            Path(__file__).resolve().parent.parent
            / "asset"
            / filename
        )

        try:
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)
        except (pygame.error, OSError) as error:
            print(f"Audio indisponivel: {error}")

    def run(self):
        try:
            while True:
                self.play_music("Menu.mp3")
                menu = Menu(self.window)
                option = menu.run()

                if option == "EXIT":
                    break

                if option in ("1 PLAYER", "2 PLAYERS"):
                    self.play_music("Level1.mp3")
                    level = Level(
                        self.window,
                        "Level1",
                        option
                    )

                    active_level = level
                    result = level.run()

                    if result == "NEXT_LEVEL":
                        self.play_music("Level2.mp3")
                        level2 = Level(self.window, "Level2", option)
                        level2.score = level.score
                        for previous, current in zip(
                            level.players, level2.players
                        ):
                            current.lives = previous.lives
                            current.last_damage_time = previous.last_damage_time
                        active_level = level2
                        result = level2.run()

                    if result == "GAME_OVER":
                        self.play_music("Score.mp3")

                        score_screen = Score(
                            self.window,
                            active_level.score,
                            option,
                            active_level.level_name
                        )

                        result = score_screen.run()

                    if result == "EXIT":
                        break
        finally:
            pygame.quit()