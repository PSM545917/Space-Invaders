import os
import pytest
from src.managers.score_manager import ScoreManager
from src.settings import HIGH_SCORE_FILE

@pytest.fixture(autouse=True)
def clean_highscore_file():
    """Limpia el archivo de récord antes y después de cada test de puntuación."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            os.remove(HIGH_SCORE_FILE)
        except IOError:
            pass
    yield
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            os.remove(HIGH_SCORE_FILE)
        except IOError:
            pass

def test_add_points_increases_score() -> None:
    """Verifica que add_points incremente el puntaje actual."""
    manager = ScoreManager()
    assert manager.score == 0
    
    manager.add_points(100)
    assert manager.score == 100

def test_high_score_updates_when_exceeded() -> None:
    """Verifica que el high_score se actualice si el score actual lo supera."""
    manager = ScoreManager()
    manager.high_score = 500
    
    manager.add_points(600)
    assert manager.high_score == 600

def test_high_score_not_updated_when_lower() -> None:
    """Verifica que el high_score no se modifique si el score actual es menor."""
    manager = ScoreManager()
    manager.high_score = 500
    
    manager.add_points(400)
    assert manager.high_score == 500

def test_high_score_persists_to_file() -> None:
    """Verifica que el récord se escriba en el archivo de texto y se cargue correctamente."""
    # Guardar récord de 1000
    manager1 = ScoreManager()
    manager1.add_points(1000)
    manager1.save_high_score()
    
    assert os.path.exists(HIGH_SCORE_FILE)
    
    # Crear un nuevo manager para cargar desde el archivo
    manager2 = ScoreManager()
    assert manager2.high_score == 1000
