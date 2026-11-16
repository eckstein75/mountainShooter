import pygame
from pathlib import Path
from code.Entity import Entity


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.speed = 5
        self.shots = []
        self.last_shot = 0
        self.shot_delay = 300
        self.lives = 3
        self.damage_cooldown = 1500
        self.last_damage_time = -1500

        image_path = (
            Path(__file__).resolve().parent.parent
            / "asset"
            / f"{name}Shot.png"
        )

        self.shot_image = pygame.image.load(
            str(image_path)
        ).convert_alpha()

    def take_damage(self):
        now = pygame.time.get_ticks()

        if (
            self.lives > 0
            and now - self.last_damage_time >= self.damage_cooldown
        ):
            self.lives -= 1
            self.last_damage_time = now
            return True

        return False

    def move(self):
        keys = pygame.key.get_pressed()

        if self.name == "Player1":
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
            if keys[pygame.K_s]:
                self.rect.y += self.speed
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed

            shooting = keys[pygame.K_SPACE]

        else:
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed

            shooting = keys[pygame.K_RCTRL]

        screen = pygame.display.get_surface()

        if screen:
            self.rect.clamp_ip(screen.get_rect())

            now = pygame.time.get_ticks()

            if shooting and now - self.last_shot >= self.shot_delay:
                shot_rect = self.shot_image.get_rect(
                    midleft=self.rect.midright
                )

                self.shots.append(shot_rect)
                self.last_shot = now

            for shot in self.shots[:]:
                shot.x += 10

                if shot.left >= screen.get_width():
                    self.shots.remove(shot)
                else:
                    screen.blit(self.shot_image, shot)