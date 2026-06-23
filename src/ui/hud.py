import arcade
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class HUD:
    """Clase auxiliar para dibujar el HUD (Heads-Up Display) en la pantalla de juego."""

    def draw(self, score: int, lives: int, wave: int) -> None:
        """Dibuja la puntuación, las vidas restantes y la oleada actual."""
        # Puntaje (esquina superior izquierda)
        arcade.draw_text(
            f"SCORE: {score}",
            x=20,
            y=SCREEN_HEIGHT - 30,
            color=arcade.color.WHITE,
            font_size=16,
            anchor_x="left",
            anchor_y="center",
        )

        # Vidas (esquina superior derecha)
        arcade.draw_text(
            f"LIVES: {lives}",
            x=SCREEN_WIDTH - 20,
            y=SCREEN_HEIGHT - 30,
            color=arcade.color.WHITE,
            font_size=16,
            anchor_x="right",
            anchor_y="center",
        )

        # Oleada (esquina inferior izquierda)
        arcade.draw_text(
            f"WAVE: {wave}",
            x=20,
            y=20,
            color=arcade.color.WHITE,
            font_size=14,
            anchor_x="left",
            anchor_y="center",
        )
