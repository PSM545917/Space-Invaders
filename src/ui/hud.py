import arcade
import os
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, ASSET_PATHS

class HUD:
    """Clase auxiliar para dibujar el HUD (Heads-Up Display) en la pantalla de juego."""

    def __init__(self) -> None:
        """Inicializa el HUD e intenta registrar la fuente pixel del proyecto."""
        self.font_name: str = "Arial"
        try:
            font_path = ASSET_PATHS["fonts"]["pixel"]
            if os.path.exists(font_path):
                arcade.load_font(font_path)
                self.font_name = "Press Start 2P"
        except Exception:
            self.font_name = "Arial"

    def draw(self, score: int, lives: int, wave: int) -> None:
        """Dibuja la puntuación, las vidas restantes y la oleada actual."""
        # Puntaje (esquina superior izquierda)
        arcade.draw_text(
            f"SCORE: {score}",
            x=20,
            y=SCREEN_HEIGHT - 30,
            color=arcade.color.WHITE,
            font_size=12 if self.font_name == "Press Start 2P" else 16,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="center",
        )

        # Vidas (esquina superior derecha)
        arcade.draw_text(
            f"LIVES: {lives}",
            x=SCREEN_WIDTH - 20,
            y=SCREEN_HEIGHT - 30,
            color=arcade.color.WHITE,
            font_size=12 if self.font_name == "Press Start 2P" else 16,
            font_name=self.font_name,
            anchor_x="right",
            anchor_y="center",
        )

        # Oleada (esquina inferior izquierda)
        arcade.draw_text(
            f"WAVE: {wave}",
            x=20,
            y=20,
            color=arcade.color.WHITE,
            font_size=10 if self.font_name == "Press Start 2P" else 14,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="center",
        )
