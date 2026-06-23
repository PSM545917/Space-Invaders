import arcade
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class MenuView(arcade.View):
    """Vista de menú inicial del juego."""

    def on_show_view(self) -> None:
        """Se ejecuta al mostrar esta vista. Configura el fondo."""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self) -> None:
        """Dibuja el título y las instrucciones en la pantalla."""
        self.clear()
        arcade.draw_text(
            "SPACE INVADERS",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2 + 50,
            color=arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
        )
        arcade.draw_text(
            "Presiona ENTER para comenzar",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2 - 50,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Maneja el inicio del juego al presionar ENTER o la salida al presionar ESC."""
        if key == arcade.key.ENTER:
            from src.game import GameView
            game_view = GameView()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            self.window.close()
