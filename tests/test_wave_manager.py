from src.managers.wave_manager import WaveManager
from src.settings import ENEMY_SPEED_BASE, ENEMY_ROWS, ENEMY_COLS

def test_next_wave_increments_counter() -> None:
    """Verifica que llamar a next_wave incremente el contador de oleada."""
    manager = WaveManager()
    assert manager.current_wave == 1
    
    manager.next_wave()
    assert manager.current_wave == 2

def test_enemy_speed_increases_per_wave() -> None:
    """Verifica que la velocidad aumente en cada nueva oleada (dificultad progresiva)."""
    manager = WaveManager()
    
    manager.start_wave(1)
    speed_w1 = manager.current_speed
    assert speed_w1 == ENEMY_SPEED_BASE

    manager.start_wave(2)
    speed_w2 = manager.current_speed
    assert speed_w2 > speed_w1
    assert speed_w2 == ENEMY_SPEED_BASE * 1.20

    manager.next_wave()
    speed_w3 = manager.current_speed
    assert speed_w3 > speed_w2
    assert speed_w3 == ENEMY_SPEED_BASE * 1.40

def test_start_wave_creates_new_formation() -> None:
    """Verifica que start_wave cree una EnemyFormation válida."""
    manager = WaveManager()
    formation = manager.start_wave(1)
    
    assert formation is not None
    assert manager.formation is formation
    # Confirmar cantidad de enemigos instanciada según settings
    assert len(formation.enemies) == ENEMY_ROWS * ENEMY_COLS
