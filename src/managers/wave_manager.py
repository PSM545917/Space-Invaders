from src.settings import ENEMY_SPEED_BASE, ENEMY_ROWS, ENEMY_COLS
from src.entities.enemy import EnemyFormation

class WaveManager:
    """Administra el progreso de las oleadas del juego y el incremento de dificultad."""

    def __init__(self) -> None:
        """Inicializa el manejador de oleadas."""
        self.current_wave: int = 1
        self.current_speed: float = ENEMY_SPEED_BASE
        self.formation: EnemyFormation | None = None

    def start_wave(self, wave_number: int) -> EnemyFormation:
        """Inicializa la oleada indicada, creando una formación con velocidad escalada."""
        self.current_wave = wave_number
        # Aumentar la velocidad en 20% acumulativo por oleada a partir de la primera
        speed_multiplier = 1.0 + (wave_number - 1) * 0.20
        self.current_speed = ENEMY_SPEED_BASE * speed_multiplier
        
        self.formation = EnemyFormation(ENEMY_ROWS, ENEMY_COLS, self.current_speed)
        return self.formation

    def next_wave(self) -> EnemyFormation:
        """Incrementa el contador de oleada e inicia el siguiente nivel."""
        return self.start_wave(self.current_wave + 1)
