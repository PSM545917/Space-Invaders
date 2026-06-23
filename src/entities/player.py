import arcade
from src.settings import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    PLAYER_LIVES,
    PLAYER_COOLDOWN,
    PLAYER_START_Y,
    SCREEN_WIDTH,
)
from src.entities.bullet import Bullet

class Player(arcade.SpriteSolidColor):
    """Representa la nave del jugador, controlando su movimiento, vidas y disparos."""

    def __init__(self) -> None:
        """Inicializa al jugador en la posición inicial, con vidas y cooldown en cero."""
        # TODO: Reemplazar el SpriteSolidColor por una textura de sprite en la Fase 5
        super().__init__(width=PLAYER_WIDTH, height=PLAYER_HEIGHT, color=arcade.color.GREEN)
        self.center_x: float = SCREEN_WIDTH / 2
        self.center_y: float = PLAYER_START_Y
        self.lives: int = PLAYER_LIVES
        self.cooldown_timer: float = 0.0

    def update(self, delta_time: float = 1/60) -> None:
        """Actualiza la posición del jugador aplicando limites y decrementa el temporizador de disparo."""
        # Manejo de cooldown de disparo
        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time
            if self.cooldown_timer < 0:
                self.cooldown_timer = 0.0

        # Mover jugador
        self.center_x += self.change_x * delta_time

        # Clampeado de bordes para evitar salir de la pantalla y detención de velocidad
        half_width = self.width / 2
        if self.center_x - half_width < 0:
            self.center_x = half_width
            if self.change_x < 0:
                self.change_x = 0.0
        elif self.center_x + half_width > SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH - half_width
            if self.change_x > 0:
                self.change_x = 0.0

    def move_left(self) -> None:
        """Establece la velocidad del jugador hacia la izquierda."""
        self.change_x = -PLAYER_SPEED

    def move_right(self) -> None:
        """Establece la velocidad del jugador hacia la derecha."""
        self.change_x = PLAYER_SPEED

    def stop_moving(self) -> None:
        """Detiene el movimiento del jugador."""
        self.change_x = 0.0

    def can_shoot(self) -> bool:
        """Retorna True si el temporizador de cooldown llegó a cero."""
        return self.cooldown_timer <= 0

    def shoot(self) -> Bullet:
        """Crea y retorna un proyectil del jugador, reiniciendo el cooldown de disparo."""
        self.cooldown_timer = PLAYER_COOLDOWN
        bullet = Bullet(owner="player", direction=1)
        bullet.center_x = self.center_x
        bullet.center_y = self.top
        return bullet
