import os
from src.settings import HIGH_SCORE_FILE

class ScoreManager:
    """Administra el puntaje del jugador y la persistencia del récord histórico (high score)."""

    def __init__(self) -> None:
        """Inicializa los puntajes y carga el récord histórico de forma segura."""
        self.score: int = 0
        self.high_score: int = 0
        self._load_high_score()

    def _load_high_score(self) -> None:
        """Carga el récord desde un archivo de texto plano. Cero si no existe o falla."""
        try:
            if os.path.exists(HIGH_SCORE_FILE):
                with open(HIGH_SCORE_FILE, "r") as file:
                    content = file.read().strip()
                    if content:
                        self.high_score = int(content)
        except (IOError, ValueError):
            # En caso de error de lectura o formato corrupto, se inicia en 0
            self.high_score = 0

    def add_points(self, points: int) -> None:
        """Acumula puntos y actualiza el récord si el puntaje actual lo supera."""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def save_high_score(self) -> None:
        """Persiste el récord histórico en el archivo de texto plano si el puntaje actual lo superó."""
        try:
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(self.high_score))
        except IOError:
            # Silenciar errores de escritura de I/O de acuerdo con las especificaciones
            pass
