import arcade
import os
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, ASSET_PATHS
from src.ui.menu_view import MenuView

def main() -> None:
    """Función principal que arranca el juego."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    # Cargar fuente pixel de forma segura
    try:
        font_path = ASSET_PATHS["fonts"]["pixel"]
        if os.path.exists(font_path):
            arcade.load_font(font_path)
    except Exception:
        pass
        
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
