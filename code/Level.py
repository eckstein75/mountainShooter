import random
import pygame
from pathlib import Path

from code.EntityFactory import EntityFactory


class Level:
    def __init__(self, window, level_name="Level1", game_mode="1 PLAYER"):
        self.window = window
        self.level_name = level_name
        self.game_mode = game_mode
        self.clock = pygame.time.Clock()
        self.score = 0
        self.font = pygame.font.Font(None, 30)

        self.backgrounds = []
        self.players = []
        self.enemies = []
        self.enemy_shots = []
        asset_dir = Path(__file__).resolve().parent.parent / "asset"
        self.enemy_shot_images = {
            name: pygame.image.load(
                str(asset_dir / f"{name}Shot.png")
            ).convert_alpha()
            for name in ("Enemy1", "Enemy2")
        }

        self.load_backgrounds()
        self.create_players()

    def load_backgrounds(self):
        asset_path = Path(__file__).resolve().parent.parent / "asset"
        width, height = self.window.get_size()

        index = 0

        while (asset_path / f"{self.level_name}Bg{index}.png").exists():
            name = f"{self.level_name}Bg{index}"

            for x in (0, width):
                background = EntityFactory.get_entity(name, (x, 0))

                background.surf = pygame.transform.scale(
                    background.surf, (width, height)
                )
                background.rect = background.surf.get_rect(
                    topleft=(x, 0)
                )

                self.backgrounds.append(background)

            index += 1

    def create_players(self):
        width, height = self.window.get_size()

        player1 = EntityFactory.get_entity(
            "Player1", (50, height // 2)
        )
        self.players.append(player1)

        if self.game_mode == "2 PLAYERS":
            player2 = EntityFactory.get_entity(
                "Player2", (100, height // 2 + 80)
            )
            self.players.append(player2)

    def create_enemy(self):
        width, height = self.window.get_size()

        name = random.choice(["Enemy1", "Enemy2"])
        position = (
            width,
            random.randint(20, max(20, height - 100))
        )

        enemy = EntityFactory.get_entity(name, position)
        self.enemies.append(enemy)
        shot_image = self.enemy_shot_images[name]
        shot_rect = shot_image.get_rect(
            midright=enemy.rect.midleft
        )
        self.enemy_shots.append({
            "rect": shot_rect,
            "image": shot_image
        })

    def check_collisions(self):
        for enemy in self.enemies[:]:
            destroyed = False

            # Verificar tiros contra inimigos
            for player in self.players:
                for shot in player.shots[:]:
                    if shot.colliderect(enemy.rect):
                        player.shots.remove(shot)
                        self.enemies.remove(enemy)
                        self.score += 10
                        destroyed = True
                        break

                if destroyed:
                    break

            if destroyed:
                continue

            # Verificar inimigos contra jogadores
            for player in self.players:
                if player.lives > 0 and enemy.rect.colliderect(player.rect):
                    self.enemies.remove(enemy)
                    player.take_damage()
                    break

    def draw_score(self):
        score_text = self.font.render(
            f"SCORE: {self.score}",
            True,
            (255, 255, 255)
        )

        self.window.blit(score_text, (10, 10))

        for index, player in enumerate(self.players):
            lives_text = self.font.render(
                f"P{index + 1} LIVES: {player.lives}",
                True,
                (255, 255, 255)
            )
            self.window.blit(lives_text, (395, 10 + index * 25))

    def run(self):
        last_spawn = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "EXIT"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "MENU"

            self.window.fill((0, 0, 0))

            for background in self.backgrounds:
                background.move()
                self.window.blit(
                    background.surf, background.rect
                )

            for player in self.players:
                if player.lives <= 0:
                    continue
                player.move()
                elapsed = pygame.time.get_ticks() - player.last_damage_time
                blink_interval = 120

                if (
                    elapsed >= player.damage_cooldown
                    or (elapsed // blink_interval) % 2 == 0
                ):
                    self.window.blit(player.surf, player.rect)

            if pygame.time.get_ticks() - last_spawn >= (900 if self.level_name == "Level2" else 1500):
                self.create_enemy()
                last_spawn = pygame.time.get_ticks()

            for enemy in self.enemies[:]:
                enemy.move()

                if enemy.rect.right < 0:
                    self.enemies.remove(enemy)

            self.check_collisions()

            if self.level_name == "Level1" and self.score >= 100:
                return "NEXT_LEVEL"

            for enemy in self.enemies:
                self.window.blit(enemy.surf, enemy.rect)

            for shot in self.enemy_shots[:]:
                speed = 7 if self.level_name == "Level2" else 5
                shot["rect"].x -= speed

                hit_player = next(
                    (
                        player for player in self.players
                        if player.lives > 0
                        and shot["rect"].colliderect(player.rect)
                    ),
                    None
                )
                if hit_player is not None:
                    self.enemy_shots.remove(shot)
                    hit_player.take_damage()
                    continue

                if shot["rect"].right < 0:
                    self.enemy_shots.remove(shot)
                else:
                    self.window.blit(
                        shot["image"], shot["rect"]
                    )

            self.draw_score()

            if all(player.lives <= 0 for player in self.players):
                overlay = pygame.Surface(
                    self.window.get_size(), pygame.SRCALPHA
                )
                overlay.fill((0, 0, 0, 180))
                self.window.blit(overlay, (0, 0))

                width, height = self.window.get_size()

                font = pygame.font.Font(None, 60)
                title = font.render(
                    "GAME OVER", True, (255, 50, 50)
                )
                self.window.blit(
                    title,
                    title.get_rect(
                        center=(width // 2, height // 2 - 30)
                    )
                )

                font_small = pygame.font.Font(None, 25)
                message = font_small.render(
                    "ENTER: Voltar ao menu",
                    True, (255, 255, 255)
                )
                self.window.blit(
                    message,
                    message.get_rect(
                        center=(width // 2, height // 2 + 25)
                    )
                )

                pygame.display.flip()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return "EXIT"

                        if event.type == pygame.KEYDOWN:
                            if event.key in (
                                pygame.K_RETURN, pygame.K_ESCAPE
                            ):
                                return "GAME_OVER"

                    self.clock.tick(30)

            pygame.display.flip()
            self.clock.tick(60)