"""Constantes globales para el juego Space Invaders.

Define dimensiones de pantalla, velocidades y configuraciones de las entidades.
"""

# Configuración de la pantalla
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
SCREEN_TITLE: str = "Space Invaders"

# Parámetros del Jugador
PLAYER_SPEED: float = 350.0
PLAYER_LIVES: int = 3
PLAYER_COOLDOWN: float = 0.4  # Tiempo mínimo entre disparos en segundos
PLAYER_START_Y: float = 50.0  # Posición Y inicial del jugador en pantalla
PLAYER_WIDTH: int = 50
PLAYER_HEIGHT: int = 30

# Parámetros de Balas
BULLET_SPEED: float = 600.0
BULLET_WIDTH: int = 6
BULLET_HEIGHT: int = 15

# Parámetros de Enemigos
ENEMY_SPEED_BASE: float = 60.0
ENEMY_ROWS: int = 5
ENEMY_COLS: int = 10
ENEMY_DESCEND_AMOUNT: float = 20.0  # Cuánto baja la formación al cambiar de dirección
ENEMY_WIDTH: int = 40
ENEMY_HEIGHT: int = 25
ENEMY_SPACING_X: float = 20.0
ENEMY_SPACING_Y: float = 20.0
ENEMY_START_X: float = 80.0
ENEMY_START_Y: float = 350.0
ENEMY_POINTS: dict[int, int] = {
    0: 10,  # Fila inferior
    1: 20,
    2: 20,
    3: 30,
    4: 30,  # Fila superior
}

# Parámetros de Barreras
BARRIER_HP: int = 4
BARRIER_WIDTH: int = 40
BARRIER_HEIGHT: int = 20

# Persistencia de Datos
HIGH_SCORE_FILE: str = "highscore.txt"

# Rutas de Recursos (Assets)
ASSET_PATHS: dict[str, dict[str, str]] = {
    "sprites": {
        "player": "assets/sprites/player_ship.png",
        "enemy": "assets/sprites/enemy_ship.png",
        "player_bullet": "assets/sprites/player_bullet.png",
        "enemy_bullet": "assets/sprites/enemy_bullet.png",
    },
    "sounds": {
        "shoot": "assets/sounds/shoot.wav.wav",
        "explosion": "assets/sounds/explosion.wav",
        "gameover": "assets/sounds/gameover.wav",
        "music": "assets/sounds/music.wav",
    },
    "fonts": {
        "pixel": "assets/fonts/PressStart2P-Regular.ttf",
    },
}
