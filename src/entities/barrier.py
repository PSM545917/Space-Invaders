import arcade
from src.settings import BARRIER_WIDTH, BARRIER_HEIGHT, BARRIER_HP

class Barrier(arcade.SpriteSolidColor):
    """Representa un escudo protector destructible."""

    def __init__(self, x: float, y: float) -> None:
        """Inicializa la barrera en la posición (x, y) con vida máxima y color verde."""
        # TODO: Reemplazar el SpriteSolidColor por una textura de sprite en la Fase 5
        super().__init__(width=BARRIER_WIDTH, height=BARRIER_HEIGHT, color=arcade.color.GREEN)
        self.center_x = x
        self.center_y = y
        self.hp: int = BARRIER_HP

    def take_damage(self, amount: int = 1) -> None:
        """Resta vida a la barrera, cambia su color según el daño, y la elimina si llega a cero."""
        self.hp -= amount
        if self.hp <= 0:
            self.remove_from_sprite_lists()
        else:
            # Cambiar color según la salud restante para indicar nivel de daño
            if self.hp == 3:
                self.color = arcade.color.YELLOW
            elif self.hp == 2:
                self.color = arcade.color.ORANGE
            elif self.hp == 1:
                self.color = arcade.color.RED
