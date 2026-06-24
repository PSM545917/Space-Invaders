import arcade
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class GameOverView(arcade.View):
    """Vista de pantalla de fin de juego (derrota o victoria)."""

    def __init__(self, score: int, high_score: int) -> None:
        """Inicializa la vista y almacena el puntaje final y el récord histórico."""
        super().__init__()
        self.score: int = score
        self.high_score: int = high_score

    def on_show_view(self) -> None:
        """Se ejecuta al mostrar esta vista. Configura el fondo."""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self) -> None:
        """Dibuja el texto de Game Over, los puntajes y la instrucción de reinicio."""
        self.clear()
        
        # Título
        arcade.draw_text(
            "GAME OVER",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2 + 100,
            color=arcade.color.RED,
            font_size=32,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        # Puntaje Final
        arcade.draw_text(
            f"Puntaje Final: {self.score}",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2,
            color=arcade.color.WHITE,
            font_size=12,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        # Récord Histórico
        arcade.draw_text(
            f"Récord Histórico: {self.high_score}",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2 - 40,
            color=arcade.color.YELLOW,
            font_size=12,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        # Instrucciones de reinicio
        arcade.draw_text(
            "Presiona R para reiniciar | ESC para salir",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2 - 120,
            color=arcade.color.LIGHT_GRAY,
            font_size=10,
            font_name="Press Start 2P",
            anchor_x="center",
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Maneja el reinicio del juego al presionar R o la salida al presionar ESC."""
        if key == arcade.key.R:
            from src.game import GameView
            game_view = GameView()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            self.window.close()
