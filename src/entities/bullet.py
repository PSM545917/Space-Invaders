import arcade
from src.settings import BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED, SCREEN_HEIGHT

class Bullet(arcade.SpriteSolidColor):
    """Representa un proyectil disparado por el jugador o por un enemigo."""

    def __init__(self, owner: str, direction: int) -> None:
        """Inicializa la bala con color según el dueño y velocidad según dirección."""
        # TODO: Reemplazar el SpriteSolidColor por una textura de sprite en la Fase 5
        color = arcade.color.YELLOW if owner == "player" else arcade.color.RED
        super().__init__(width=BULLET_WIDTH, height=BULLET_HEIGHT, color=color)
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
