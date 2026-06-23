import arcade
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from src.ui.menu_view import MenuView

def main() -> None:
    """Función principal que arranca el juego."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
