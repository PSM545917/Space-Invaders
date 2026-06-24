import arcade
from src.settings import BULLET_SPEED, BULLET_WIDTH, SCREEN_HEIGHT, ASSET_PATHS

class Bullet(arcade.Sprite):
    """Representa un proyectil disparado por el jugador o por un enemigo."""

    def __init__(self, owner: str, direction: int) -> None:
        """Inicializa la bala con textura escalada a BULLET_WIDTH según el dueño."""
        sprite_key = "player_bullet" if owner == "player" else "enemy_bullet"
        texture = arcade.load_texture(ASSET_PATHS["sprites"][sprite_key])
        scale = BULLET_WIDTH / texture.width
        super().__init__(texture, scale=scale)
        self.owner: str = owner
        self.change_y: float = direction * BULLET_SPEED

    def update(self, delta_time: float = 1/60) -> None:
        """Mueve el proyectil y lo elimina si sale de los límites de la pantalla."""
        self.center_y += self.change_y * delta_time

        # Si sale de la pantalla por arriba o por abajo, se auto-elimina
        if self.bottom > SCREEN_HEIGHT or self.top < 0:
            self.remove_from_sprite_lists()

    def reset(self, x: float, y: float, direction: int) -> None:
        """Reposiciona y reactiva el proyectil para su reuso en el pool."""
        self.center_x = x
        self.center_y = y
        self.change_y = direction * BULLET_SPEED
